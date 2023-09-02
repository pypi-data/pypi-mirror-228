# -*- coding: utf-8 -*-

"""

tests.test_nodes

Test the serializable_trees.nodes module

Copyright (C) 2023 Rainer Schwarzbach

This file is part of serializable_trees.

serializable_trees is free software:
you can redistribute it and/or modify it under the terms of the MIT License.

serializable_trees is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

import copy
import re

from unittest import TestCase

import yaml

from serializable_trees import nodes


# List of leaves

LI_LV_SRC = """---
- abcd
- 7
- 2.375
- true
- null
"""

LI_LV_TARGET = nodes.ListNode(
    [
        "abcd",
        7,
        2.375,
        True,
        None,
    ]
)

# Map of leaves

MA_LV_SRC = """---
7: abcd
2.375: 7
yes: 2.375
null: true
abcd: null
"""

MA_LV_TARGET = nodes.MapNode(
    {
        7: "abcd",
        2.375: 7,
        True: 2.375,
        None: True,
        "abcd": None,
    }
)

SIMPLE_YAML = """levels:
  one:
    two:
      three_1:
      - a
      - b
      - c
      three_2: 999
    four: 4.0
    more: original data
"""

MERGE_YAML = """levels:
  one:
    two:
      three_1:
      - g
      - h
      - i
      three_3: new leaf
    more: changed data
xxx: yyy
"""

EXPECTED_MERGE_RESULT_LIST_EXTEND_YAML = """levels:
  one:
    two:
      three_1:
      - a
      - b
      - c
      - g
      - h
      - i
      three_2: 999
      three_3: new leaf
    four: 4.0
    more: changed data
xxx: yyy
"""

EXPECTED_MERGE_RESULT_LIST_REPLACE_YAML = """levels:
  one:
    two:
      three_1:
      - g
      - h
      - i
      three_2: 999
      three_3: new leaf
    four: 4.0
    more: changed data
xxx: yyy
"""


class NodeTest(TestCase):

    """Node base class"""

    def test_deepcopy(self):
        """__deepcopy__ special method"""
        base_node = nodes.Node([])
        self.assertRaises(
            NotImplementedError,
            copy.deepcopy,
            base_node,
        )

    def test_eq(self):
        """__eq__ special method"""
        node_1 = nodes.Node([1, 2, 3])
        node_2 = nodes.Node([1, 2, 3])
        node_3 = nodes.Node([7, 5, 9])
        node_4 = nodes.Node([200, 20, 12, 13])
        with self.subTest("not implemented", case="equal"):
            self.assertRaises(
                NotImplementedError,
                node_1.__eq__,
                node_2,
            )
        #
        with self.subTest("not implemented", case="same length"):
            self.assertRaises(
                NotImplementedError,
                node_1.__eq__,
                node_3,
            )
        #
        with self.subTest("not equal", case="different length"):
            self.assertNotEqual(node_1, node_4)
        #


class ImprovedListNodeTest(TestCase):

    """ListNode class improved test cases"""

    def test_eq(self):
        """__eq__ special method"""
        base_node = nodes.ListNode(["a", "b", "c"])
        equal_node = nodes.ListNode(["a", "b", "c"])
        other_length_node = nodes.ListNode(["x", "y"])
        other_order_node = nodes.ListNode(["c", "b", "a"])
        other_type_node = nodes.MapNode({0: "a", 1: "b", 2: "c"})
        with self.subTest("equal"):
            self.assertEqual(base_node, equal_node)
        #
        with self.subTest("not equal", case="different length"):
            self.assertNotEqual(base_node, other_length_node)
        #
        with self.subTest("not equal", case="different order"):
            self.assertNotEqual(base_node, other_order_node)
        #
        with self.subTest("not equal", case="different type"):
            self.assertNotEqual(base_node, other_type_node)
        #

    def test_deepcopy(self):
        """__deepcopy__ special method"""
        base_node = nodes.ListNode(
            [
                nodes.ListNode([1, 2, 3]),
                nodes.ListNode(["s", "b", "c"]),
            ]
        )
        nested_list_copy = copy.deepcopy(base_node)
        with self.subTest("base node", scope="equality"):
            self.assertEqual(nested_list_copy, base_node)
        #
        with self.subTest("base node", scope="identity"):
            self.assertIsNot(nested_list_copy, base_node)
        #
        for key, item in enumerate(base_node):
            with self.subTest("child node", scope="equality", key=key):
                self.assertEqual(nested_list_copy[key], item)
            #
            with self.subTest("child node", scope="identity", key=key):
                self.assertIsNot(nested_list_copy[key], item)
            #
        #

    def test_setitem(self):
        """__setitem__() special method"""
        base_node = nodes.ListNode([nodes.ListNode(["abc"])])
        with self.subTest("regular item setting"):
            base_node[0] = nodes.ListNode(["def"])
            self.assertEqual(base_node[0][0], "def")
        #
        with self.subTest("circular growth", scope="child"):
            self.assertRaisesRegex(
                nodes.CircularGrowthException,
                "^Circular reference detected in"
                r" ListNode\(\[ListNode\(\['def'\]\)\]\)",
                base_node.__setitem__,
                0,
                base_node,
            )
        #
        with self.subTest("circular growth", scope="grandchild"):
            self.assertRaisesRegex(
                nodes.CircularGrowthException,
                r"^Circular reference detected in ListNode\(\['def'\]\)",
                base_node[0].__setitem__,
                0,
                base_node,
            )
        #

    def test_append(self):
        """append() method"""
        base_node = nodes.ListNode([nodes.ListNode(["abc"])])
        with self.subTest("regular append"):
            base_node.append(nodes.ListNode(["def"]))
            self.assertEqual(base_node[1][0], "def")
        #
        with self.subTest("circular growth", scope="child"):
            self.assertRaisesRegex(
                nodes.CircularGrowthException,
                "^Circular reference detected in"
                r" ListNode\(\[ListNode\(\['abc'\]\),"
                r" ListNode\(\['def'\]\)\]\)",
                base_node.append,
                base_node,
            )
        #
        with self.subTest("circular growth", scope="grandchild"):
            self.assertRaisesRegex(
                nodes.CircularGrowthException,
                r"^Circular reference detected in ListNode\(\['abc'\]\)",
                base_node[0].append,
                base_node,
            )
        #

    def test_insert(self):
        """insert() method"""
        base_node = nodes.ListNode([nodes.ListNode(["abc"])])
        with self.subTest("regular insert"):
            base_node.insert(0, nodes.ListNode(["def"]))
            self.assertEqual(
                base_node,
                nodes.ListNode(
                    [
                        nodes.ListNode(["def"]),
                        nodes.ListNode(["abc"]),
                    ]
                ),
            )
        #
        with self.subTest("circular growth", scope="child"):
            self.assertRaisesRegex(
                nodes.CircularGrowthException,
                "^Circular reference detected in"
                r" ListNode\(\[ListNode\(\['def'\]\),"
                r" ListNode\(\['abc'\]\)\]\)",
                base_node.insert,
                1,
                base_node,
            )
        #
        with self.subTest("circular growth", scope="grandchild"):
            self.assertRaisesRegex(
                nodes.CircularGrowthException,
                r"^Circular reference detected in ListNode\(\['def'\]\)",
                base_node[0].insert,
                0,
                base_node,
            )
        #


class ImprovedMapNodeTest(TestCase):

    """MapNode class improved test cases"""

    def test_deepcopy(self):
        """__deepcopy__ special method"""
        base_node = nodes.MapNode(
            abcd=nodes.MapNode(one=1, two=2, seven=7),
            efgh=nodes.MapNode({9: "nine", True: "yes"}),
        )
        nested_list_copy = copy.deepcopy(base_node)
        with self.subTest("base node", scope="equality"):
            self.assertEqual(nested_list_copy, base_node)
        #
        with self.subTest("base node", scope="identity"):
            self.assertIsNot(nested_list_copy, base_node)
        #
        for key in base_node:
            with self.subTest("child node", scope="equality", key=key):
                self.assertEqual(nested_list_copy[key], base_node[key])
            #
            with self.subTest("child node", scope="identity", key=key):
                self.assertIsNot(nested_list_copy[key], base_node[key])
            #
        #

    def test_setitem(self):
        """__setitem__() special method"""
        base_node = nodes.MapNode(first=nodes.MapNode(value="abc"))
        with self.subTest("regular item setting"):
            base_node["second"] = nodes.ListNode(["xyz"])
            self.assertEqual(base_node.second[0], "xyz")
        #
        with self.subTest("circular growth", scope="child"):
            self.assertRaisesRegex(
                nodes.CircularGrowthException,
                "^Circular reference detected in"
                f" {re.escape(repr(base_node))}",
                base_node.__setitem__,
                "third",
                base_node,
            )
        #
        with self.subTest("circular growth", scope="grandchild"):
            self.assertRaisesRegex(
                nodes.CircularGrowthException,
                "^Circular reference detected in"
                f" {re.escape(repr(base_node.second))}",
                base_node.second.__setitem__,
                0,
                base_node,
            )
        #
        with self.subTest("circular growth", scope="greatgrandchild"):
            ancestor = nodes.MapNode(child=base_node)
            self.assertRaisesRegex(
                nodes.CircularGrowthException,
                "^Circular reference detected in"
                f" {re.escape(repr(base_node.first))}",
                base_node.first.__setitem__,
                "loop",
                ancestor,
            )
        #


class ListTest(TestCase):

    """ListNode instance"""

    def test_simple_list_nodes(self):
        """simple ListNode test"""
        source_data = yaml.safe_load(LI_LV_SRC)
        full_branch = nodes.grow_branch(source_data)
        with self.subTest("full test"):
            self.assertEqual(full_branch, LI_LV_TARGET)
        #
        for key, value in enumerate(source_data):
            with self.subTest("item test", key=key):
                self.assertEqual(full_branch[key], value)
            #
        #
        with self.subTest("back to native test"):
            self.assertEqual(nodes.native_types(full_branch), source_data)
        #
        with self.subTest("pop test", target="value"):
            self.assertEqual(full_branch.pop(0), source_data[0])
        #
        with self.subTest("pop test", target="length"):
            self.assertEqual(len(full_branch) + 1, len(source_data))
        #
        with self.subTest("inequality test", target="length"):
            self.assertNotEqual(full_branch, source_data)
        #
        with self.subTest("append test", target="value"):
            full_branch.append("tail value")
            self.assertEqual(full_branch[-1], "tail value")
        #
        with self.subTest("contains test", target="contents"):
            self.assertTrue("tail value" in full_branch)
        #
        with self.subTest("append test", target="length"):
            self.assertEqual(len(full_branch), len(source_data))
        #
        with self.subTest("inequality test", target="contents"):
            self.assertNotEqual(full_branch, source_data)
        #
        with self.subTest("insert test", target="value"):
            full_branch.insert(0, "head value")
            self.assertEqual(full_branch[0], "head value")
        #
        with self.subTest("insert test", target="equality"):
            self.assertEqual(full_branch[1:-1], source_data[1:])
        #
        with self.subTest("invalid test", target="message"):
            self.assertRaisesRegex(
                nodes.ItemTypeInvalid,
                "^ListNode items must be either"
                " scalar values or Node instances",
                full_branch.append,
                [1, 2, 3],
            )
        #
        with self.subTest("delete test", target="length"):
            del full_branch[0]
            self.assertEqual(len(full_branch), len(source_data))
        #

    def test_list_nodes_errors(self):
        """ListNode errors test"""
        full_branch = nodes.ListNode(["abc", "def"])
        with self.subTest("invalid item set", target="message"):
            self.assertRaisesRegex(
                nodes.ItemTypeInvalid,
                "^ListNode items must be either"
                " scalar values or Node instances",
                full_branch.__setitem__,
                1,
                [1, 2, 3],
            )
        #
        with self.subTest("invalid item inserted", target="message"):
            self.assertRaisesRegex(
                nodes.ItemTypeInvalid,
                "^ListNode items must be either"
                " scalar values or Node instances",
                full_branch.insert,
                0,
                [1, 2, 3],
            )
        #
        with self.subTest("invalid init", target="message"):
            self.assertRaisesRegex(
                nodes.ItemTypeInvalid,
                "^ListNode items must be either"
                " scalar values or Node instances",
                nodes.ListNode,
                [1, 2, 3, [4, 5]],
            )
        #


class MapTest(TestCase):

    """MapNode classes"""

    def test_simple_map_nodes(self):
        """simple MapNode test"""
        source_data = yaml.safe_load(MA_LV_SRC)
        full_branch = nodes.grow_branch(source_data)
        with self.subTest("full test"):
            self.assertEqual(full_branch, MA_LV_TARGET)
        #
        for key, value in source_data.items():
            with self.subTest("item test", key=key):
                self.assertEqual(full_branch[key], value)
            #
        #
        with self.subTest("namespace test", attr="abcd"):
            self.assertEqual(full_branch.abcd, source_data["abcd"])
        #
        with self.subTest("back to native test"):
            self.assertEqual(nodes.native_types(full_branch), source_data)
        #
        with self.subTest("pop test", key="abcd", scope="value"):
            self.assertEqual(
                nodes.map_node_pop(full_branch, "abcd"), source_data["abcd"]
            )
        #
        with self.subTest("pop test", key="abcd", scope="attribute"):
            self.assertRaises(
                AttributeError,
                getattr,
                full_branch,
                "abcd",
            )
        #
        with self.subTest("inequality test", target="length"):
            self.assertNotEqual(full_branch, source_data)
        #
        with self.subTest("contains test", target="negative"):
            self.assertFalse("abcd" in full_branch)
        #
        with self.subTest("setattr test", attr="abcd"):
            full_branch.abcd = "abcd replacement"
            self.assertEqual(full_branch.abcd, "abcd replacement")
        #
        with self.subTest("inequality test", target="contents"):
            self.assertNotEqual(full_branch, source_data)
        #
        with self.subTest("contains test", target="positive"):
            self.assertTrue("abcd" in full_branch)
        #
        with self.subTest("delete test", key="abcd", scope="attribute"):
            del full_branch.abcd
            self.assertRaises(
                AttributeError,
                getattr,
                full_branch,
                "abcd",
            )
        #

    def test_map_nodes_errors(self):
        """MapNode errors test"""
        with self.subTest("invalid init (direct)", target="message"):
            self.assertRaisesRegex(
                nodes.ItemTypeInvalid,
                "^MapNode items must be either"
                " scalar values or Node instances",
                nodes.MapNode,
                {"valid": 1, "invalid": [4, 5]},
            )
        #
        with self.subTest("invalid init (direct)", target="message"):
            self.assertRaisesRegex(
                nodes.ItemTypeInvalid,
                "^MapNode items must be either"
                " scalar values or Node instances",
                nodes.MapNode,
                {"valid1": 1, "valid2": None},
                invalid_kwargs_item=[7, 8, 9],
            )
        #
        full_branch = nodes.MapNode(one=1, two=2)
        with self.subTest("delete non-existing attribute", target="message"):
            self.assertRaisesRegex(
                AttributeError,
                "^MapNode instance has no attribute 'three'",
                full_branch.__delattr__,
                "three",
            )
        #
        with self.subTest("set invalid attribute", target="message"):
            self.assertRaisesRegex(
                nodes.ItemTypeInvalid,
                "^MapNode items must be either"
                " scalar values or Node instances",
                full_branch.__setattr__,
                "invalid3",
                [1, 7, 5],
            )
        #


class HelperFunctionsTest(TestCase):

    """Helper functions"""

    def test_grow_branch(self):
        """grow_branch() function"""
        with self.subTest("invalid branch grow item", target="message"):
            self.assertRaises(
                TypeError,
                nodes.grow_branch,
                [1, 2, 3, set([1, 3])],
            )
        #

    def test_merge_branches(self):
        """merge_branches() function"""
        full_branch = nodes.grow_branch(yaml.safe_load(SIMPLE_YAML))
        to_merge_branch = nodes.grow_branch(yaml.safe_load(MERGE_YAML))
        with self.subTest("extend lists strategy"):
            result_branch = nodes.merge_branches(
                full_branch, to_merge_branch, extend_lists=True
            )
            self.assertEqual(
                result_branch,
                nodes.grow_branch(
                    yaml.safe_load(EXPECTED_MERGE_RESULT_LIST_EXTEND_YAML)
                ),
            )
        #
        with self.subTest("replace lists strategy"):
            result_branch = nodes.merge_branches(
                full_branch, to_merge_branch, extend_lists=False
            )
            self.assertEqual(
                result_branch,
                nodes.grow_branch(
                    yaml.safe_load(EXPECTED_MERGE_RESULT_LIST_REPLACE_YAML)
                ),
            )
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
