################################################################################
#                                 py-fast-trie                                 #
#          Python library for tries with different grades of fastness          #
#                       (C) 2020, 2022-2023 Jeremy Brown                       #
#                Released under Prosperity Public License 3.0.0                #
################################################################################


from numbers import Integral
from struct import pack, unpack
from sys import maxsize
from test import (
    invalid_trie_entry,
    max_trie_entry_size,
    max_trie_value,
    valid_int_entries,
    valid_int_entry,
    valid_trie_entries,
    valid_trie_entry,
)

import pytest

from hypothesis import given, settings
from hypothesis.stateful import RuleBasedStateMachine, invariant, rule
from hypothesis.strategies import integers, lists

from py_fast_trie import XFastTrie


def to_bytes(val):
    if val.bit_length() < 9:
        fmt = "B"
    elif val.bit_length() < 17:
        fmt = ">H"
    elif val.bit_length() < 33:
        fmt = ">L"
    else:
        fmt = ">Q"

    return pack(fmt, val)


@given(integers(min_value=0, max_value=max_trie_entry_size))
def test_make_level_tables(depth):
    assert len(XFastTrie._make_level_tables(depth)) == depth


@given(valid_trie_entry)
def test_to_int(value):
    if isinstance(value, int):
        assert XFastTrie._to_int(value, max_trie_entry_size) == value

    elif isinstance(value, bytes):
        value_int = unpack(">Q", value.rjust((maxsize.bit_length() + 1) // 8, b"\x00"))[
            0
        ]
        assert XFastTrie._to_int(value, max_trie_entry_size) == value_int


@given(invalid_trie_entry)
def test_to_int_exceptions(value):
    if isinstance(value, Integral):
        with pytest.raises(ValueError):
            XFastTrie._to_int(value, max_trie_entry_size)

    elif isinstance(value, bytes):
        with pytest.raises(ValueError):
            XFastTrie._to_int(value, max_trie_entry_size)

    else:
        with pytest.raises(TypeError):
            XFastTrie._to_int(value, max_trie_entry_size)


@given(valid_trie_entries, valid_int_entries)
def test_get_closest_ancestor(entries, test_values):
    t = XFastTrie(max_trie_entry_size)

    for entry in entries:
        t += entry

    entries = [t._to_int(e, t._maxlen) for e in entries]

    for val in test_values:
        ancestor, level = t._get_closest_ancestor(val)

        if val in entries:
            assert ancestor.leaf
            assert ancestor.value == val

        else:
            assert not ancestor.leaf
            test_bits = bin(val)[2:].zfill(t._maxlen)[: level + 2]

            left_desc_lvl = t._maxlen if ancestor.left.leaf else level + 2
            assert (
                not bin(ancestor.left.value)[2:]
                .zfill(left_desc_lvl)
                .startswith(test_bits)
            )

            right_desc_lvl = t._maxlen if ancestor.right.leaf else level + 2
            assert (
                not bin(ancestor.right.value)[2:]
                .zfill(right_desc_lvl)
                .startswith(test_bits)
            )


@given(valid_trie_entries, valid_int_entries)
def test_get_closest_leaf(entries, test_values):
    t = XFastTrie(max_trie_entry_size)

    for entry in entries:
        t += entry

    entries = [t._to_int(e, t._maxlen) for e in entries]

    for val in test_values:
        neighbor = t._get_closest_leaf(val)
        assert neighbor.leaf

        if val in entries:
            assert neighbor.value == val

        else:
            if neighbor.left is not None:
                assert abs(neighbor.value - val) <= abs(neighbor.left.value - val)

            if neighbor.right is not None:
                assert abs(neighbor.value - val) <= abs(neighbor.right.value - val)


@given(valid_trie_entries, valid_int_entries)
def test_predecessor(entries, test_values):
    t = XFastTrie(max_trie_entry_size)

    for entry in entries:
        t += entry

    for val in test_values:
        pred = t < val

        if pred is not None:
            assert pred < val
            pred = t.predecessor(val)

            if pred.right is not None:
                assert pred.right.value >= val


@given(valid_trie_entries, valid_int_entries)
def test_successor(entries, test_values):
    t = XFastTrie(max_trie_entry_size)

    for entry in entries:
        t += entry

    for val in test_values:
        succ = t > val

        if succ is not None:
            assert succ > val
            succ = t.successor(val)

            if succ.left is not None:
                assert succ.left.value <= val


def test_successor_predecessor_empty_trie():
    t = XFastTrie(max_trie_entry_size)

    with pytest.raises(ValueError):
        t.successor(0)

    with pytest.raises(ValueError):
        t.predecessor(0)


@given(valid_trie_entries)
def test_clear(entries):
    t = XFastTrie(max_trie_entry_size)

    for entry in entries:
        t += entry

    assert len(t) > 0
    assert t._min is not None
    assert t._max is not None

    t.clear()

    for d in t._level_tables:
        assert len(d) == 0

    assert len(t) == 0
    assert t._min is None
    assert t._max is None


@given(lists(valid_int_entry, min_size=0, max_size=max_trie_value, unique=True))
def test_iter(entries):
    t = XFastTrie(max_trie_entry_size)

    for entry in entries:
        t += entry

    entries = sorted(entries)

    for entry in t:
        assert entry == entries.pop(0)

    assert len(entries) == 0


class XFastStateMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.t = XFastTrie(max_trie_entry_size)

    def teardown(self):
        values = list(self.t._level_tables[-1])

        for val in values:
            self.t -= val

    @invariant()
    def valid_count(self):
        assert len(self.t) == len(self.t._level_tables[-1])

    @invariant()
    def valid_min(self):
        if len(self.t) > 0:
            assert self.t._min.left is None

            for leaf in self.t._level_tables[-1].values():
                assert leaf is self.t._min or self.t.min < leaf.value

    @invariant()
    def valid_max(self):
        if len(self.t) > 0:
            assert self.t._max.right is None

            for leaf in self.t._level_tables[-1].values():
                assert leaf is self.t._max or self.t.max > leaf.value

    @invariant()
    def valid_pointers(self):
        for level, table in enumerate(self.t._level_tables):
            for node in table.values():
                if not node.leaf:
                    left_child_value = node.value << 1 & -2
                    right_child_value = node.value << 1 | 1
                    left_child = self.t._level_tables[level + 1].get(left_child_value)
                    right_child = self.t._level_tables[level + 1].get(right_child_value)

                    # While we're in here, make sure the node should be in the trie
                    assert left_child is not None or right_child is not None

                    if left_child is not None:
                        assert node.left is left_child
                        assert left_child.parent is node
                    else:
                        desc = node.right

                        while not desc.leaf:
                            desc = desc.left

                        assert node.left is desc

                    if right_child is not None:
                        assert node.right is right_child
                        assert right_child.parent is node
                    else:
                        desc = node.left

                        while not desc.leaf:
                            desc = desc.right

                        assert node.right is desc
                else:
                    if node.left is not None:
                        assert node.left.value < node.value

                    if node.right is not None:
                        assert node.right.value > node.value

    @rule(val=valid_trie_entry)
    def insert_value(self, val):
        self.t += val

    @rule(val=valid_trie_entry)
    def remove_value(self, val):
        if val not in self.t:
            try:
                self.t -= val
            except ValueError:
                pass
        else:
            self.t -= val


XFastStateMachine.TestCase.settings = settings(max_examples=50, deadline=None)
test_x_fast_trie = XFastStateMachine.TestCase
