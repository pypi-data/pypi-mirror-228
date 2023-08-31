################################################################################
#                                 py-fast-trie                                 #
#          Python library for tries with different grades of fastness          #
#                       (C) 2020, 2022-2023 Jeremy Brown                       #
#                Released under Prosperity Public License 3.0.0                #
################################################################################

from py_fast_trie.x_fast import TrieNode


def test_init():
    left = TrieNode("left", True)
    right = TrieNode("right", True)
    par = TrieNode("parent", False, left, right)

    assert left.value == "left"
    assert left.leaf is True
    assert left.left is None
    assert left.right is None
    assert left.parent is None

    assert right.value == "right"
    assert right.leaf is True
    assert right.left is None
    assert right.right is None
    assert right.parent is None

    assert par.value == "parent"
    assert par.leaf is False
    assert par.left is left
    assert par.right is right
    assert par.parent is None
