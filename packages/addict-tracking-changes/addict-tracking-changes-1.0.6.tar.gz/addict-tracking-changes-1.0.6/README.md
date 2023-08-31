# [addict-tracking-changes](https://github.com/Monallabs-org/addict-tracking-changes)


[![Python versions](https://img.shields.io/badge/Python-3.11-green)](https://pypi.python.org/pypi/addict-tracking-changes)
[![Tests Status](https://github.com/ofjustpy/addict-tracking-changes/blob/main/badge_tests.svg)](https://github.com/ofjustpy/addict-tracking-changes/actions)
[![Coverage Status](https://github.com/ofjustpy/addict-tracking-changes/blob/main/badge_coverage.svg)](https://github.com/ofjustpy/addict-tracking-changes/actions)
[![Flake8 Status](https://github.com/ofjustpy/addict-tracking-changes/blob/main/badge_flake8.svg)](https://github.com/ofjustpy/addict-tracking-changes/actions)

[![Documentation](https://img.shields.io/badge/doc-latest-blue.svg)](https://ofjustpy.github.io/addict-tracking-changes/)
[![PyPI](https://img.shields.io/pypi/v/addict-tracking-changes.svg)](https://pypi.python.org/pypi/addict-tracking-changes)
[![Downloads](https://pepy.tech/badge/addict-tracking-changes)](https://pepy.tech/project/addict-tracking-changes)
[![Downloads per week](https://pepy.tech/badge/addict-tracking-changes/week)](https://pepy.tech/project/addict-tracking-changes)
[![GitHub stars](https://img.shields.io/github/stars/ofjustpy/addict-tracking-changes.svg)](https://github.com/ofjustpy/addict-tracking-changes/stargazers)


## Introduction

**HEADS UP** 
Before using the library carefully read the Known bugs and Caveats section below. 


Originally, this repository was a fork of [addict](https://github.com/mewwts/addict) by Mats Julian Olsen.
Overtime, it has substatially diverged in functionality and codebase that it made
sense to breakout as its own repository. 

The original addict:  provides an alternative and succient interface to manipulate a dictionary. This is especially
useful when dealing with heavily nested dictionaries. As example (taken from https://github.com/mewwts/addict)
a dictionary created using standard python dictionary interface looks as follows:
```python
body = {
    'query': {
        'filtered': {
            'query': {
                'match': {'description': 'addictive'}
            },
            'filter': {
                'term': {'created_by': 'Mats'}
            }
        }
    }
}`

``` 
can be summarized to following three lines:

```python
body = Dict()
body.query.filtered.query.match.description = 'addictive'
body.query.filtered.filter.term.created_by = 'Mats'
```

This repo builds on original addict and adds contraptions to track key additions in the dictionary.
This features comes in quite handy in building reactive webapps where one has to respond 
to all the changes made on the browser. Addict-tracking-changes is the underpinning
data-structure in [ofjustpy](https://github.com/Monallabs-org/ofjustpy): a python based webframework build from [justpy](https://github.com/justpy-org/justpy)
 
The functions relevant to tracking changed history are:
`get_changed_history` and `clear_changed_history`. 
The `get_changed_history` returns an iterator of XPath style paths like `/a/b/c/e` (see [Demo example](#demo-example)). 

## Usage and examples

### Installation
This project is not on PyPI. Its a simple package with no third party dependency. 
Simply clone from github and include the source directory in your PYTHONPATH. 

### Demo example

```python
from addict import Dict
body = Dict()
body.query.filtered.query.match.description = 'addictive'
body.query.filtered.filter.term.created_by = 'Mats'

for changed_path in body.get_changed_history():
    #<work with changed_path>

body.clear_changed_history()
```

### Behaviour when values are instances of container types 
addict works as expected when the values of keys are simple data types (such as string, int, float, etc.). However, for container types such as dict, list, tuples, etc. the behaviour is somewhat differs. 

* dicts are treated as opaque object just like simple data types

```python
from addict import Dict

mydict = Dict()
mydict.a.b.c = {'kk': 1}
mydict.a.b.e = {'dd': 1}

for _ in mydict.get_changed_history():
    print(_) 
```
will print
```
/a/b/c
/a/b/e
```
and not 
```
/a/b/cc/kk
/a/b/e/dd
```

* lists
are seen as container, i.e., `get_changed_history` will report path for each element of
the list 

```python
from addict import Dict

mydict = Dict()

mydict.a.b = [1, [1]]
mydict.a.c = [2, [2, [3]]]
```
get_changed_history will report following paths:
```
/a/b/0,
/a/b/1/0,
/a/c/0,
/a/c/1/0,
/a/c/1/1/"
```

* tuple, namedtuple, sets
tuple  behave same as dict and are treated as opaque data structure


## Known bugs and Caveats
1. Only tracks  field additions.  Deletions and updates are not tracked. 
2. freeze doesn't guards against deletions
3. building dict from another dict as shown in following expression wont' work
```python
cjs_cfg = Dict(other_dict, track_changes=True)
```
instead use
```python 
cjs_cfg = Dict(track_changes = True)
with open("other_dict.pickle", "rb") as fh:
    x = pickle.load(fh)
for _ in oj.dictWalker(x):
    oj.dnew(cjs_cfg, _[0], _[1])

```
4. Use TrackedList for tracking nested list

```python
from addict_tracking_changes import Dict, TrackedList


trackerprop = Dict(track_changes = True)
trackerprop.a.b = [1, TrackedList([1], track_changes=True)]
trackerprop.a.c = [2, TrackedList([2, TrackedList([3], track_changes=True)
                                   ], track_changes=True)
                   ]
```
which when asked changed history will output as follows:
```python
print(list(trackerprop.get_changed_history()))
```
output
```bash
['/a/b/0', '/a/b/1/0', '/a/c/0', '/a/c/1/0', '/a/c/1/1/0']
```


## APIs
| API                                                  | Description                                        |
|------------------------------------------------------|----------------------------------------------------|
| `Dict(*args, **kwargs)`                              | Initializes a new Dict object                      |
| `to_dict(self)`                                      | Converts the Dict object to a regular dictionary   |
| `freeze(self, shouldFreeze=True)`                    | Freezes the Dict object, making it immutable       |
| `unfreeze(self)`                                     | Unfreezes the Dict object, making it mutable again |
| `get_changed_history(self, prefix="", path_guards=None)` | Returns an iterator with the changed history of keys |
| `clear_changed_history(self)`                        | Clears the changed history of the Dict object      |
| `set_tracker(self, track_changes=False)`             | Sets or resets the change tracker for the Dict object |



### EndNotes
- Docs (in readthedocs format): https://monallabs-org.github.io/addict-tracking-changes/#introduction, https://webworks.monallabs.in/addict-tracking-changes

- Developed By: webworks.monallabs.in

