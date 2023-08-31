################################################################################
#                                 py-fast-trie                                 #
#          Python library for tries with different grades of fastness          #
#                       (C) 2020, 2022-2023 Jeremy Brown                       #
#                Released under Prosperity Public License 3.0.0                #
################################################################################

from __future__ import annotations

from collections.abc import Iterable
from sys import maxsize
from typing import Optional, cast

from py_hopscotch_dict import HopscotchDict


class TrieNode:
    __slots__ = (
        "leaf",
        "left",
        "parent",
        "right",
        "value",
    )

    def __init__(
        self,
        value: Optional[int],
        leaf: bool,
        left: Optional[TrieNode] = None,
        right: Optional[TrieNode] = None,
    ) -> None:
        self.leaf = leaf
        self.left = left
        self.parent: Optional[TrieNode] = None
        self.right = right
        self.value = value


class XFastTrie:
    __slots__ = (
        "_count",
        "_level_tables",
        "_max",
        "_maxlen",
        "_min",
        "_root",
    )

    @staticmethod
    def _make_level_tables(levels: int) -> list[HopscotchDict]:
        """
        Creates the dicts used when searching for a value in the trie

        :param levels: The number of levels in the trie
        :return: Search structures for each level of the trie
        """
        return [HopscotchDict() for _ in range(levels)]

    @staticmethod
    def _to_int(value: int | bytes, length: int) -> int:
        """
        Confirm the desired value could be contained in the table,
        then perform any necessary conversions to the canonical value format

        :param value: The value to be converted
        :param length: The maximum bit length of a value in the trie
        :return: The value converted to an int
        """
        if isinstance(value, int):
            if value.bit_length() > length:
                raise ValueError("Value is too big to be stored in trie")
            elif value < 0:
                raise ValueError("Negative values cannot be stored in trie")
            else:
                return value

        elif isinstance(value, bytes):
            if len(value) * 8 > length:
                raise ValueError("Value is too big to be stored in trie")

            else:
                return sum(map(lambda t: t[1] << 8 * t[0], enumerate(reversed(value))))

        else:
            raise TypeError("Only integers and byte sequences can be stored in trie")

    def clear(self) -> None:
        """
        Empty the trie of all values
        """
        self._count = 0
        self._level_tables = self._make_level_tables(self._maxlen)
        self._min: Optional[TrieNode] = None
        self._max: Optional[TrieNode] = None
        self._root = TrieNode(None, False)

    def _get_closest_ancestor(self, value: int) -> tuple[TrieNode, int]:
        """
        Find the node in the trie with the longest prefix that matches the given value

        :param value: The value to search for
        :return: The node with the longest prefix matching the given value,
                 and its depth in the trie
        """
        result = self._root
        # Moving the root node out of the level tables allows for storing n-bit integers
        result_level = -1

        low_side = 0
        high_side = self._maxlen - 1

        while low_side <= high_side:
            level = (low_side + high_side) // 2
            prefix = value >> (self._maxlen - level - 1)

            if prefix not in self._level_tables[level]:
                high_side = level - 1
            else:
                result = self._level_tables[level][prefix]
                result_level = level
                low_side = level + 1

        return (result, result_level)

    def _get_closest_leaf(self, value: int) -> Optional[TrieNode]:
        """
        Find the leaf in the trie with the value closest to the given value

        :param value: The value to search for
        :return: The leaf with the closest value to the given value
        """
        result = None
        ancestor, level = self._get_closest_ancestor(value)

        # The value is stored in the trie and therefore is the closest leaf to itself
        if ancestor.leaf:
            return ancestor

        # The pointer to the next level down is a descendant pointer
        # and may be larger or smaller than the given value, depending on the leg
        else:
            leg = value >> (self._maxlen - level - 2) & 1
            descendant = ancestor.left if leg == 0 else ancestor.right

            if descendant is not None:
                # The descendant pointer only points to values
                # on the other leg of the ancestor;
                # make sure there is no leaf not a child of the ancestor which is closer
                candidate = descendant.left if leg == 0 else descendant.right

                if candidate is None or abs(cast(int, descendant.value) - value) < abs(
                    cast(int, candidate.value) - value
                ):
                    result = descendant
                else:
                    result = candidate
        return result

    def insert(self, value: int | bytes) -> None:
        """
        Add the given value to the trie

        :param value: The value to add to the trie
        """
        value = self._to_int(value, self._maxlen)

        # Do nothing if the value is already in the trie
        if value in self._level_tables[-1]:
            return

        leaf_pred = leaf_succ = None

        if self._count > 0:
            neighbor = cast(TrieNode, self._get_closest_leaf(value))

            # The closest leaf is the predecessor of the value to be inserted
            if cast(int, neighbor.value) < value:
                leaf_pred = neighbor
                leaf_succ = neighbor.right

            # The closest leaf is the successor of the value to be inserted
            elif cast(int, neighbor.value) > value:
                leaf_succ = neighbor
                leaf_pred = neighbor.left

        leaf_node = TrieNode(value, True, leaf_pred, leaf_succ)
        value_bits = bin(value)[2:].zfill(self._maxlen)

        # Get ancestor node for new intermediate nodes
        curr_node: Optional[TrieNode]
        depth: int
        curr_node, depth = self._get_closest_ancestor(value)

        for level in range(depth, self._maxlen - 1):
            desc_value = int(value_bits[: level + 2], 2)
            desc_leg = value_bits[level + 1]

            # Inserting leaf node
            if level == self._maxlen - 2:
                descendant = leaf_node

                # Update global min/max pointers as necessary
                if self._min is None or value < cast(int, self._min.value):
                    self._min = descendant

                if self._max is None or value > cast(int, self._max.value):
                    self._max = descendant

                # Wire the new leaf into the linked list at the bottom
                if leaf_pred is not None:
                    leaf_pred.right = descendant

                if leaf_succ is not None:
                    leaf_succ.left = descendant

            # Inserting intermediate node
            else:
                descendant = TrieNode(desc_value, False, None, None)

            # Point the descendant node back to its parent
            descendant.parent = curr_node

            # Point the parent at its new descendant node,
            # making descendant pointers to the new leaf as necessary
            if desc_leg == "0":
                curr_node.left = descendant

                if curr_node.right is None:
                    curr_node.right = leaf_node
            else:
                curr_node.right = descendant

                if curr_node.left is None:
                    curr_node.left = leaf_node

            self._level_tables[level + 1][desc_value] = descendant
            curr_node = descendant

        # Walk up the trie from the leaf node,
        # updating descendant pointers as necessary
        while curr_node is not None:
            if not curr_node.leaf:
                if curr_node.left.leaf and curr_node.left.value > value:  # type: ignore
                    curr_node.left = leaf_node
                elif curr_node.right.leaf and curr_node.right.value < value:  # type: ignore # noqa
                    curr_node.right = leaf_node
            curr_node = curr_node.parent

        self._count += 1

    def predecessor(self, value: int | bytes) -> Optional[TrieNode]:
        """
        Find the largest value in the trie strictly less than the given value

        :param value: The value to find the predecessor for
        :return: The leaf with the largest value strictly less than the given value,
                 or None if the value is at most the value of the smallest leaf
        """
        value = self._to_int(value, self._maxlen)
        node = self._get_closest_leaf(value)

        # This should only happen if there are no values in the trie,
        # But if it could also happen because of some unconsidered edge case,
        # make some noise so the edge case can be fixed
        if node is None:
            raise ValueError("No values exist in trie")
        else:
            return node.left if cast(int, node.value) >= value else node

    def remove(self, value: int | bytes) -> None:
        """
        Remove the given value from the trie

        :param value: The value to remove from the trie
        """
        value = self._to_int(value, self._maxlen)
        curr_node = self._level_tables[-1].get(value)

        # Error when trying to remove a value that hasn't been added
        if curr_node is None:
            raise ValueError("Value does not exist in trie")
        else:
            leaf_pred = curr_node.left
            leaf_succ = curr_node.right
            curr_level = self._maxlen - 1

            # Walk up the trie from the leaf node,
            # modifying/removing internal nodes as necessary
            while curr_node is not None:
                parent = curr_node.parent
                should_delete = False

                # Removing leaf node
                if curr_node.leaf:
                    should_delete = True

                    # Remove the node from the linked list
                    if leaf_pred is not None:
                        leaf_pred.right = leaf_succ

                    if leaf_succ is not None:
                        leaf_succ.left = leaf_pred

                # Root updates
                elif parent is None:
                    if cast(TrieNode, self._min).value == value:
                        self._min = leaf_succ

                    if cast(TrieNode, self._max).value == value:
                        self._max = leaf_pred

                # Removing intermediate nodes
                else:
                    valid_left = valid_right = False

                    if curr_node.left is not None:
                        ptr_level = -1 if curr_node.left.leaf else curr_level + 1
                        if curr_node.left.value in self._level_tables[ptr_level]:
                            valid_left = True

                    if curr_node.right is not None:
                        ptr_level = -1 if curr_node.right.leaf else curr_level + 1
                        if curr_node.right.value in self._level_tables[ptr_level]:
                            valid_right = True

                    should_delete = not (valid_left or valid_right)

                # Trim pointers between the target node at the start of this loop,
                # its parent and its descendants
                if should_delete:
                    node_bits = bin(curr_node.value)[2:].zfill(curr_level + 1)
                    if node_bits[-1] == "0":
                        parent.left = None

                        if parent.right == curr_node:
                            parent.right = None
                    else:
                        parent.right = None

                        if parent.left == curr_node:
                            parent.left = None

                    del self._level_tables[curr_level][curr_node.value]
                    curr_node.left = curr_node.right = curr_node.parent = None
                    del curr_node

                # Update dangling descendant pointers for remaining intermediate nodes
                else:
                    if curr_node.left is None or (
                        curr_node.left.leaf and curr_node.left.value == value
                    ):
                        curr_node.left = leaf_succ

                    if curr_node.right is None or (
                        curr_node.right.leaf and curr_node.right.value == value
                    ):
                        curr_node.right = leaf_pred

                curr_node = parent
                curr_level -= 1

        self._count -= 1

    def successor(self, value: int | bytes) -> Optional[TrieNode]:
        """
        Find the smallest value in the trie strictly greater than the given value

        :param value: The value to find the successor for
        :return: The leaf with the smallest value strictly greater than the given value,
                 or None if the value is at least the value of the largest leaf
        """
        value = self._to_int(value, self._maxlen)
        node = self._get_closest_leaf(value)

        # This should only happen if there are no values in the trie,
        # But if it could also happen because of some unconsidered edge case,
        # make some noise so the edge case can be fixed
        if node is None:
            raise ValueError("No values exist in trie")
        else:
            return node.right if cast(int, node.value) <= value else node

    @property
    def max(self) -> Optional[int]:
        """
        The maximum value in the trie

        :return: The maximum value in the trie,
                 or None if the trie is empty
        """
        return self._max.value if self._max is not None else self._max

    @property
    def min(self) -> Optional[int]:
        """
        The minimum value in the trie

        :return: The minimum value in the trie,
                 or None if the trie is empty
        """
        return self._min.value if self._min is not None else self._min

    def __init__(self, max_length: int = (maxsize.bit_length() + 1)) -> None:
        self._maxlen = max_length
        self.clear()

    def __contains__(self, value: int | bytes) -> bool:
        value = self._to_int(value, self._maxlen)
        return value in self._level_tables[-1]

    def __gt__(self, value: int | bytes) -> Optional[int]:
        result = self.successor(value)
        return result.value if result is not None else result

    def __iadd__(self, value: int | bytes) -> XFastTrie:
        self.insert(value)
        return self

    def __isub__(self, value: int | bytes) -> XFastTrie:
        self.remove(value)
        return self

    def __iter__(self) -> Iterable[int]:
        node = self._min
        while node is not None:
            yield cast(int, node.value)
            node = node.right

    def __len__(self) -> int:
        return self._count

    def __lt__(self, value: int | bytes) -> Optional[int]:
        result = self.predecessor(value)
        return result.value if result is not None else result
