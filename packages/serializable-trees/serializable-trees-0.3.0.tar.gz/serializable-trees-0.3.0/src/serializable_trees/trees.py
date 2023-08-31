# -*- coding: utf-8 -*-

"""

serializable_trees.trees

TraversalPath and Tree data types

Copyright (C) 2023 Rainer Schwarzbach

This file is part of serializable_trees.

serializable_trees is free software:
you can redistribute it and/or modify it under the terms of the MIT License.

serializable_trees is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import json

from collections.abc import Hashable
from typing import List, Dict, Optional, Tuple, Union

import yaml

from serializable_trees import nodes


DEFAULT_INDENT = 2


class TraversalPath:

    """A traversal path"""

    def __init__(self, *components: Hashable) -> None:
        """store the components internally"""
        self.__components: Tuple[Hashable, ...] = components

    def __len__(self) -> int:
        """Return the length of the components"""
        return len(self.__components)

    def __repr__(self) -> str:
        """Return a string representation"""
        return (
            f"{self.__class__.__name__}"
            f"({', '.join(repr(item) for item in self.__components)})"
        )

    def traverse(
        self,
        start: Union[Hashable, nodes.Node],
    ) -> Union[Hashable, nodes.Node]:
        """Traverse through a branch starting at the start node,
        and return the node or Hashable at the end point
        """
        pointer = start
        for key in self.__components:
            if isinstance(pointer, nodes.Node):
                pointer = pointer[key]
            else:
                raise TypeError("Cannot traverse through a leaf")
            #
        #
        return pointer

    def partial_walk(
        self,
        start: nodes.Node,
        fail_on_missing_keys: bool = True,
        minimum_remaining_components: int = 1,
    ) -> Tuple[nodes.Node, List[Hashable]]:
        """Traverse through a branch starting at the start node,
        and ending minimum_remaining_components before the-last path component.
        If fail_on_missing_keys is True (default setting),
        re-raise the keyError on missing keys. If it is set to false,
        end the walk just before the missing key.
        Return a tuple containing the last node encountered
        and the remaining path component(s).
        """
        if len(self) < minimum_remaining_components:
            raise IndexError(
                f"A minimum of {minimum_remaining_components}"
                f" path component(s) is required, but got only {len(self)}^"
            )
        #
        pointer: Union[Hashable, nodes.Node] = start
        remaining_components = list(self.__components)
        while len(remaining_components) > minimum_remaining_components:
            if not isinstance(pointer, nodes.Node):
                raise TypeError("Cannot walk through a leaf")
            #
            key = remaining_components[0]
            try:
                pointer = pointer[key]
            except KeyError as error:
                if fail_on_missing_keys:
                    raise KeyError(key) from error
                #
                break
            else:
                del remaining_components[0]
            #
        #
        if isinstance(pointer, nodes.Node):
            return (pointer, remaining_components)
        #
        raise TypeError(
            "End point seems to be a leaf instead of a Node instance"
        )


class Tree:

    """A tree consisting of Nodes and Hashables"""

    def __init__(self, root: Union[Hashable, nodes.Node]) -> None:
        """Set the root node"""
        if not isinstance(root, (Hashable, nodes.Node)):
            raise nodes.ItemTypeInvalid(self)
        #
        self.root: Union[Hashable, nodes.Node] = root

    def __eq__(self, other) -> bool:
        """True if both root objects are equal"""
        return self.root == other.root

    def __repr__(self) -> str:
        """Return a string representation"""
        return f"{self.__class__.__name__}({repr(self.root)})"

    def crop(
        self,
        path: TraversalPath,
    ) -> Union[Hashable, nodes.Node]:
        """Remove and return the item determined by the path
        (hint: "crop" rhymes with "pop").
        The result can be a partial tree (= a branch of nested
        nodes.Node instances) or a leaf (= a hashable value).
        Might re-raise a KeyError from the underlying Node object
        """
        if not isinstance(self.root, nodes.Node):
            # Allow cropping a leaf at the root node
            # only with an empty path – seplace the root by an empty
            # MapNode in that case.
            if path:
                raise TypeError("Cannot walk through a leaf")
            #
            root_leaf = self.root
            self.root = nodes.MapNode()
            return root_leaf
        #
        parent_node, remaining_components = path.partial_walk(
            self.root, fail_on_missing_keys=True
        )
        last_key = remaining_components[0]
        if isinstance(parent_node, nodes.ListNode):
            if isinstance(last_key, int):
                value = parent_node.pop(last_key)
            else:
                raise TypeError(
                    "ListNode keys must be int,"
                    f" not {last_key.__class__.__name__}"
                )
            #
        elif isinstance(parent_node, nodes.MapNode):
            value = nodes.map_node_pop(parent_node, last_key)
        else:
            # Hypothetical branch for the type checker
            raise TypeError(  # NOT TESTABLE
                "The result must be either a ListNode or MapNode"
            )
        #
        return value

    def get_native_item(
        self, path: TraversalPath
    ) -> Union[Hashable, Dict, List]:
        """Return the native type of the item determined by the path.
        The result can be a list, dict, or Hashable,
        or any combination of them.
        Might re-raise a KeyError from the underlying Node object
        """
        return nodes.native_types(path.traverse(self.root))

    def get_clone(self, path: TraversalPath) -> Union[Hashable, nodes.Node]:
        """Return a deep copy of the item determined by the path.
        The result can be a partial tree (= a branch of nested
        nodes.Node instances) or a leaf (= a hashable value).
        Might re-raise a KeyError from the underlying Node object
        """
        return nodes.grow_branch(self.get_native_item(path))

    def graft(
        self,
        path: TraversalPath,
        sprout: Union[Hashable, nodes.Node],
    ) -> None:
        """Add a sprout on top of the specified path."""
        if not isinstance(self.root, nodes.Node):
            # Do not allow grafting with a leaf at the root
            raise TypeError("Cannot graft on a leaf")
        #
        last_existing_node, remaining_components = path.partial_walk(
            self.root, fail_on_missing_keys=False
        )
        if len(remaining_components) > 1:
            # build a new intermediate structure using the remaining components
            for new_key in remaining_components[:-1]:
                last_existing_node[new_key] = nodes.MapNode()
                pointer = last_existing_node[new_key]
                # Hypothetical branch for the type checker
                if isinstance(pointer, nodes.Node):
                    last_existing_node = pointer
                else:
                    raise TypeError(  # NOT TESTABLE
                        "Cannot grow a branch through a leaf"
                    )
                #
            #
        #
        last_existing_node[remaining_components[-1]] = sprout

    def joined_tree(self, other: "Tree", extend_lists: bool = False) -> "Tree":
        """Return a new tree from self and other joined (resp. merged)"""
        return self.__class__(
            nodes.merge_branches(
                self.root, other.root, extend_lists=extend_lists
            )
        )

    def truncate(self, path: Optional[TraversalPath] = None) -> None:
        """Truncate the tree at (below) the specified path"""
        if path is None:
            path = TraversalPath()
        #
        if not isinstance(self.root, nodes.Node):
            # Do not allow a leaf at the root with a path
            if path:
                raise TypeError(
                    f"Cannot truncate using path {path} with a leaf root"
                )
            #
            self.root = nodes.MapNode()
            return
        #
        last_remaining_node = path.traverse(self.root)
        if isinstance(last_remaining_node, Hashable):
            parent_node, keys = path.partial_walk(self.root)
            parent_node[keys[0]] = nodes.MapNode()
        elif isinstance(last_remaining_node, nodes.ListNode):
            while last_remaining_node:
                last_remaining_node.pop()
            #
        elif isinstance(last_remaining_node, nodes.MapNode):
            keys = list(last_remaining_node)
            for single_key in keys:
                nodes.map_node_pop(last_remaining_node, single_key)
            #
        #

    def to_json(
        self, indent: Optional[int] = DEFAULT_INDENT, sort_keys: bool = False
    ) -> str:
        """Return a JSON representation"""
        return json.dumps(
            nodes.native_types(self.root),
            ensure_ascii=True,
            indent=indent,
            sort_keys=sort_keys,
        )

    def to_yaml(
        self, indent: Optional[int] = DEFAULT_INDENT, sort_keys: bool = False
    ) -> str:
        """Return a YAML representation"""
        return yaml.safe_dump(
            nodes.native_types(self.root),
            allow_unicode=True,
            default_flow_style=False,
            indent=indent,
            sort_keys=sort_keys,
            explicit_end=False,
        )

    @classmethod
    def from_json(cls, json_serialization: str) -> "Tree":
        """Return a tree from a JSON representation"""
        return cls(nodes.grow_branch(json.loads(json_serialization)))

    @classmethod
    def from_yaml(cls, yaml_serialization: str) -> "Tree":
        """Return a tree from a YAML representation"""
        return cls(nodes.grow_branch(yaml.safe_load(yaml_serialization)))


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
