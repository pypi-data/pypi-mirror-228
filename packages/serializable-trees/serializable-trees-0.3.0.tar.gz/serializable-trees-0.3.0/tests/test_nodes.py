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

    def test_eq(self):
        """_eq_ special method"""
        base_node = nodes.Node([])
        self.assertRaises(
            NotImplementedError,
            base_node.__eq__,
            None,
        )


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
                "^ListNode items must be either hashable or Node instances",
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
                "^ListNode items must be either hashable or Node instances",
                full_branch.__setitem__,
                1,
                [1, 2, 3],
            )
        #
        with self.subTest("invalid item inserted", target="message"):
            self.assertRaisesRegex(
                nodes.ItemTypeInvalid,
                "^ListNode items must be either hashable or Node instances",
                full_branch.insert,
                0,
                [1, 2, 3],
            )
        #
        with self.subTest("invalid init", target="message"):
            self.assertRaisesRegex(
                nodes.ItemTypeInvalid,
                "^ListNode items must be either hashable or Node instances",
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
                "^MapNode items must be either hashable or Node instances",
                nodes.MapNode,
                {"valid": 1, "invalid": [4, 5]},
            )
        #
        with self.subTest("invalid init (direct)", target="message"):
            self.assertRaisesRegex(
                nodes.ItemTypeInvalid,
                "^MapNode items must be either hashable or Node instances",
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
                "^MapNode items must be either hashable or Node instances",
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
