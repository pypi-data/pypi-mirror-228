# Serializable Trees


_Easy-to-use serializable tree datatypes for Python_

## Installation


You can install the [package from PyPI](https://pypi.org/project/serializable-trees/):

```bash
pip install --upgrade serializable-trees
```

Using a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
is strongly recommended.

---
> **⚠ Please use version 0.4.0 or newer**

> In earlier releases, **Node** contents were not checked
> for circular references, which could lead to infinite loops.

> Starting with release 0.4.0, **Node** instance implement additional checks
> that prevent the creation of circular node references.

---


## Package contents and basic usage

The **serializable_trees** package contains the modules

- **serializable\_trees.nodes** implementing a low-level API
  with the **ListNode** and **MapNode** classes and some helper functions
- **serializable\_trees.trees** implementing a high-level API
  with the **TraversalPath** and **Tree** classes.

Both high-level API classes from the **[trees](module_reference/trees/)** module
are aliased in the base module so they can simply be imported using

```
>>> from serializable_trees import TraversalPath, Tree
```

Loading a data structure from a file is easy,
but its representation is a bit hard to read.

Using the `to_yaml()` or `to_json()` methods
and printing the results improves readability:

```
>>> gitlab_ci = Tree.from_file(".gitlab-ci.yml")
>>> gitlab_ci
Tree(MapNode({'include': MapNode({'project': 'blackstream-x/building-blocks', 'file': '/Pipelines/python/pip/package+docs.gitlab-ci.yml'}), 'variables': MapNode({'MODULE_NAME': 'serializable_trees'}), 'python:mypy': MapNode({'variables': MapNode({'EXTRA_REQUIREMENTS': 'types-pyyaml'})}), 'python:pylint': MapNode({'variables': MapNode({'CODESTYLE_TARGET': 'src'})})}))
>>>
>>> print(gitlab_ci.to_yaml())
include:
  project: blackstream-x/building-blocks
  file: /Pipelines/python/pip/package+docs.gitlab-ci.yml
variables:
  MODULE_NAME: serializable_trees
python:mypy:
  variables:
    EXTRA_REQUIREMENTS: types-pyyaml
python:pylint:
  variables:
    CODESTYLE_TARGET: src

>>>
```

**Tree** contents can be accessed directly under the `root` attribute:

```
>>> gitlab_ci.root.include
MapNode({'project': 'blackstream-x/building-blocks', 'file': '/Pipelines/python/pip/package+docs.gitlab-ci.yml'})
>>>
>>> gitlab_ci.root.include.project
'blackstream-x/building-blocks'
>>> gitlab_ci.root.include.file
'/Pipelines/python/pip/package+docs.gitlab-ci.yml'
>>>
```

Using **TraversalPath** objects, you can manipulate the tree.
In this case, remove a portion from the tree and return it:

```
>>> include_path = TraversalPath("include")
>>> old_include_contents = gitlab_ci.crop(include_path)
>>> old_include_contents
MapNode({'project': 'blackstream-x/building-blocks', 'file': '/Pipelines/python/pip/package+docs.gitlab-ci.yml'})
>>> print(gitlab_ci.to_yaml())
variables:
  MODULE_NAME: serializable_trees
python:mypy:
  variables:
    EXTRA_REQUIREMENTS: types-pyyaml
python:pylint:
  variables:
    CODESTYLE_TARGET: src

>>>
```

**ListNode** and **MapNode** objects can be used to define new items:

```
>>> from serializable_trees.nodes import ListNode, MapNode
>>>
>>> gitlab_ci.graft(include_path, ListNode([MapNode(template="Security/Secret-Detection.gitlab-ci.yml")]))
>>>
>>> print(gitlab_ci.to_yaml())
variables:
  MODULE_NAME: serializable_trees
python:mypy:
  variables:
    EXTRA_REQUIREMENTS: types-pyyaml
python:pylint:
  variables:
    CODESTYLE_TARGET: src
include:
- template: Security/Secret-Detection.gitlab-ci.yml

>>>
```

**ListNode** instances have an **append()** method like **list** objects:

```
>>> gitlab_ci.root.include.append(old_include_contents)
>>>
>>> print(gitlab_ci.to_yaml())
variables:
  MODULE_NAME: serializable_trees
python:mypy:
  variables:
    EXTRA_REQUIREMENTS: types-pyyaml
python:pylint:
  variables:
    CODESTYLE_TARGET: src
include:
- template: Security/Secret-Detection.gitlab-ci.yml
- project: blackstream-x/building-blocks
  file: /Pipelines/python/pip/package+docs.gitlab-ci.yml

>>>
>>> gitlab_ci.root.include
ListNode([MapNode({'template': 'Security/Secret-Detection.gitlab-ci.yml'}), MapNode({'project': 'blackstream-x/building-blocks', 'file': '/Pipelines/python/pip/package+docs.gitlab-ci.yml'})])
>>>
```

## Further reading

[→ Full documentation](https://blackstream-x.gitlab.io/serializable-trees/)

