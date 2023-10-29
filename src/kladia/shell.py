"""
In this module I want to create a shell to execute
functions defined in the module, just like Python's REPL.

The prompt for this shell is ?

For example:

? graph 'g'
g.setdefault(-1, {})

? print g
{-1: {}}

? add node 'A' to 'g'
g.setdefault('A', {-1: {}})

? print g
{-1: {}, 'A': {-1: {}}}

? add node 'B' to 'g'
g.setdefault('B', {-1: {}})

? print g
{-1: {}, 'A': {-1: {}}, 'B': {-1: {}}}

? add edge from 'A' to 'B'
g['A'].setdefault('B', {-1: {}})

? print g
{-1: {}, 'A': {-1: {}, 'B': {-1: {}}}, 'B': {-1: {}}}

? add edge from 'B' to 'A'
g['B'].setdefault('A', {-1: {}})

? print g
{-1: {}, 'A': {-1: {}, 'B': {-1: {}}}, 'B': {-1: {}, 'A': {-1: {}}}}
"""

