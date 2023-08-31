# -*- coding: utf-8 -*-

"""

serializable_trees.nodes

Node data types

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

from collections.abc import Collection, Hashable
from typing import Dict, Iterator, List, Optional, Tuple, Union


class ItemTypeInvalid(TypeError):

    """Raised on invalid item types"""

    def __init__(self, instance) -> None:
        """Initialize the super class"""
        super().__init__(
            f"{instance.__class__.__name__} items must be either hashable"
            " or Node instances."
        )


class Node(Collection):

    """Abstract collection node containing Hashables or other nodes"""

    def __init__(self, collection) -> None:
        """Store the collection internally"""
        self._internal_collection = copy.copy(collection)

    def __eq__(self, other) -> bool:
        """Return True if both Nodes are equal"""
        raise NotImplementedError

    def __iter__(self):
        """Iterator over the internal collection"""
        return iter(self._internal_collection)

    def __repr__(self):
        """String representation"""
        return f"{self.__class__.__name__}({repr(self._internal_collection)})"

    def __len__(self) -> int:
        """Length of the internal collection"""
        return len(self._internal_collection)

    def __delitem__(self, key) -> None:
        """Delete the specified item from the internal collection"""
        del self._internal_collection[key]

    def __getitem__(self, key) -> Union[Hashable, "Node"]:
        """Return the specified item from the internal collection"""
        return self._internal_collection[key]

    def __setitem__(self, key, value: Union[Hashable, "Node"]) -> None:
        """Set the specified item in the internal collection"""
        if not isinstance(value, (Hashable, Node)):
            raise ItemTypeInvalid(self)
        #
        self._internal_collection[key] = value

    def __contains__(self, item) -> bool:
        """Return true if the internal collection
        contains the specified item
        """
        return item in self._internal_collection


class ListNode(Node):

    """List node containing a list of other nodes"""

    def __init__(self, sequence) -> None:
        """Store the collection internally"""
        collection: List[Union[Hashable, Node]] = list(sequence)
        if not all(isinstance(item, (Hashable, Node)) for item in collection):
            raise ItemTypeInvalid(self)
        #
        super().__init__(collection)

    def __eq__(self, other) -> bool:
        """Return true if all members of both ListNodes are equal"""
        if len(self) != len(other):
            return False
        #
        for li_index, own_value in enumerate(self):
            if other[li_index] != own_value:
                return False
            #
        #
        return True

    def append(self, item: Union[Hashable, Node]) -> None:
        """Append an item to the internal list"""
        if isinstance(item, (Hashable, Node)):
            self._internal_collection.append(item)
        else:
            raise ItemTypeInvalid(self)
        #

    def insert(self, key: int, item: Union[Hashable, Node]) -> None:
        """Insert an item into the internal list"""
        if isinstance(item, (Hashable, Node)):
            self._internal_collection.insert(key, item)
        else:
            raise ItemTypeInvalid(self)
        #

    def pop(self, key: int = -1) -> Union[Hashable, Node]:
        """Pop an item from the internal list"""
        item = self._internal_collection.pop(key)
        if isinstance(item, (Hashable, Node)):
            return item
        #
        # Hypothetical statement for the type checker
        raise ItemTypeInvalid(self)  # NOT TESTABLE


class MapNode(Node):

    """Map node containing a dict of other nodes"""

    def __init__(self, mapping: Optional[Dict] = None, **kwargs) -> None:
        """Store the collection internally"""
        collection: Dict[Hashable, Union[Hashable, Node]] = dict(mapping or {})
        if not all(
            isinstance(item, (Hashable, Node))
            for key, item in collection.items()
        ):
            raise ItemTypeInvalid(self)
        #
        for key, value in kwargs.items():
            if not isinstance(value, (Hashable, Node)):
                raise ItemTypeInvalid(self)
            #
            collection[key] = value
        #
        super().__init__(collection)

    def __eq__(self, other) -> bool:
        """Return true if all members of both MapNodes are equal"""
        if len(self) != len(other):
            return False
        #
        for key in self:
            if other[key] != self[key]:
                return False
            #
        #
        return True

    def __getattr__(self, name: str) -> Union[Hashable, Node]:
        """Get an item (indexed by a string) as attribute"""
        try:
            return self[name]
        except KeyError as error:
            raise AttributeError(
                f"{self.__class__.__name__} instance has no attribute {name!r}"
            ) from error
        #

    def __setattr__(
        self, name: str, value: Union[Dict, Hashable, Node]
    ) -> None:
        """Set an item (indexed by a string) as attribute"""
        if (
            name == "_internal_collection"
            and isinstance(value, dict)
            and name not in self.__dict__
        ):
            self.__dict__[name] = value
        elif not isinstance(value, (Hashable, Node)):
            raise ItemTypeInvalid(self)
        else:
            self[name] = value
        #

    def __delattr__(self, name: str) -> None:
        """Delete an item (indexed by a string) from the attributes"""
        try:
            del self[name]
        except KeyError as error:
            raise AttributeError(
                f"{self.__class__.__name__} instance has no attribute {name!r}"
            ) from error
        #


#
# Module-level functions
#


def grow_branch(
    data_structure: Union[Hashable, Dict, List]
) -> Union[Hashable, Node]:
    """Factory function: return nested nodes"""
    if isinstance(data_structure, Hashable):
        return copy.deepcopy(data_structure)
    #
    if isinstance(data_structure, dict):
        return MapNode(
            {key: grow_branch(item) for key, item in data_structure.items()}
        )
    #
    if isinstance(data_structure, list):
        return ListNode(grow_branch(item) for item in data_structure)
    #
    raise TypeError(
        "Branches can only be grown from nested dicts and/or lists"
        " of hashable values."
    )


def map_node_items(
    map_node: MapNode,
) -> Iterator[Tuple[Hashable, Union[Hashable, Node]]]:
    """Return an Iterator over MapNode items"""
    for key in map_node:
        if not isinstance(key, Hashable):
            # Hypothetical branch for the type checker
            raise TypeError(  # NOT TESTABLE
                "Non-hashable dict key – should never happen"
            )
        #
        item = map_node[key]
        if not isinstance(item, (Hashable, Node)):
            # Hypothetical branch for the type checker
            raise ItemTypeInvalid(map_node)  # NOT TESTABLE
        #
        yield key, item
    #


def map_node_pop(map_node: MapNode, key: Hashable) -> Union[Hashable, Node]:
    """Return and delete an item from a map node"""
    # pylint: disable=protected-access ; required for access "from outside"
    item = map_node._internal_collection.pop(key)
    # pylint: enable=protected-access
    if not isinstance(item, (Hashable, Node)):
        # Hypothetical branch for the type checker
        raise ItemTypeInvalid(map_node)  # NOT TESTABLE
    #
    return item


def native_types(
    branch_root: Union[Hashable, Node]
) -> Union[Hashable, Dict, List]:
    """Return native types from nested Node instances"""
    if isinstance(branch_root, Hashable):
        return branch_root
    #
    if isinstance(branch_root, MapNode):
        return {
            key: native_types(item)
            for key, item in map_node_items(branch_root)
        }
    #
    if isinstance(branch_root, ListNode):
        return [native_types(item) for item in branch_root]
    #
    # Hypothetical statement for the type checker
    raise ItemTypeInvalid(branch_root)  # NOT TESTABLE


def merge_branches(
    branch_1: Union[Hashable, Node],
    branch_2: Union[Hashable, Node],
    extend_lists: bool = False,
) -> Union[Hashable, Node]:
    """Return a new branch containing branch_2
    merged into branch_1.
    """
    if isinstance(branch_1, MapNode) and isinstance(branch_2, MapNode):
        new_map = MapNode()
        seen_in_branch_2 = set()
        for key in branch_1:
            try:
                new_map[key] = merge_branches(
                    branch_1[key], branch_2[key], extend_lists=extend_lists
                )
            except KeyError:
                new_map[key] = grow_branch(native_types(branch_1[key]))
            else:
                seen_in_branch_2.add(key)
            #
        #
        for key in branch_2:
            if key in seen_in_branch_2:
                continue
            #
            new_map[key] = grow_branch(native_types(branch_2[key]))
        #
        return new_map
    #
    if isinstance(branch_1, ListNode) and isinstance(branch_2, ListNode):
        new_list = ListNode([])
        if extend_lists:
            for item in branch_1:
                new_list.append(grow_branch(native_types(item)))
            #
        #
        for item in branch_2:
            new_list.append(grow_branch(native_types(item)))
        #
        return new_list
    #
    return grow_branch(native_types(branch_2))


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
