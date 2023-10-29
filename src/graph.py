from collections import defaultdict
from typing import Dict, Hashable, Set, Callable, Tuple, Optional


# Entities
class Entity:
    def __init__(self, name: Hashable, attrs: Optional[Dict[Hashable, Dict | None]] = None):
        self.name = name
        self.attrs = attrs if attrs is not None else {}

class Table(Entity): ...

class Graph(Entity): ...

class Node(Entity): ...

class Arrow(Entity):
    def __init__(self, name: Tuple[Hashable, Hashable], attrs: Optional[Dict] = None):
        # name <- (tail, head)
        name = (name[0], name[1])
        super().__init__(name, attrs)

class Link(Entity): ...


# Data storage

tables = {}
graphs = {}
nodes = {}
arrows = {}
links = {}


# Create entities
def table(name: Hashable, attrs: Dict | None = None) -> Table:
    return Table(name, attrs)

def graph(name: Hashable, attrs: Dict | None = None) -> Graph:
    return Graph(name, attrs)


def node(name: Hashable, attrs: Dict | None = None) -> Node:
    return Node(name, attrs)


def arrow(name: Tuple[Hashable, Hashable], attrs: Dict | None = None) -> Arrow:
    return Arrow(name, attrs)


def link(name: Hashable, attrs: Dict | None = None) -> Link:
    return Link(name, attrs)


# C.R.U.D. functions.
def new(fn: Callable, name: Hashable, attrs: Dict | None = None) -> None:
    entity = fn(name, attrs)
    if isinstance(entity, Table):
        tables[name] = entity.attrs
    elif isinstance(entity, Graph):
        graphs[name] = entity.attrs
    elif isinstance(entity, Node):
        nodes[name] = entity.attrs
    elif isinstance(entity, Arrow):
        arrows[entity.name] = entity.attrs
    elif isinstance(entity, Link):
        links[name] = entity.attrs


def assign(fn: Callable, name: Hashable, attrs: Dict | Hashable) -> None:
    if fn ==table:
        tables[name] = attrs
    elif fn == graph:
        graphs[name] = attrs
    elif fn == node:
        nodes[name] = attrs
    elif fn == arrow:
        arrows[name] = attrs
    elif fn == link:
        links[name] = attrs


def read(fn: Callable, name: Hashable) -> Dict | None:
    if fn == table:
        return tables.get(name)
    elif fn == graph:
        return graphs.get(name)
    elif fn == node:
        return nodes.get(name)
    elif fn == arrow:
        return arrows.get(name)
    elif fn == link:
        return links.get(name)


def delete(fn: Callable, name: Hashable) -> None:
    if fn == table:
        tables.pop(name, None)
    elif fn == graph:
        graphs.pop(name, None)
    elif fn == node:
        nodes.pop(name, None)
    elif fn == arrow:
        arrows.pop(name, None)
    elif fn == link:
        links.pop(name, None)


# Example of use:
if __name__ == "__main__":
    new(graph, "g")
    assert read(graph, "g") == {}

    new(node, "A")
    assert read(node, "A") == {}

    assign(graph, "g", {"A": None})
    assert read(graph, "g") == {"A": None}

    new(node, "B")
    assert read(node, "B") == {}

    assign(graph, "g", {"A": None, "B": None})
    assert read(graph, "g") == {"A": None, "B": None}

    new(node, "C")
    assert read(node, "C") == {}

    assign(graph, "g", {"A": None, "B": None, "C": None})
    assert read(graph, "g") == {"A": None, "B": None, "C": None}

    new(arrow, ("A", "B"))
    assert read(arrow, ("A", "B")) == {}

    assign(graph, "g", {"A": {("A", "B"): None}, "B": None, "C": None})
    assert read(graph, "g") == {"A": {("A", "B"): None}, "B": None, "C": None}

    new(arrow, ("B", "B"))
    assert read(arrow, ("B", "B")) == {}

    assign(graph, "g", {"A": {("A", "B"): None}, "B": {("B", "B"): None}, "C": None})
    assert read(graph, "g") == {"A": {("A", "B"): None}, "B": {("B", "B"): None}, "C": None}

    new(link, "X")
    assert read(link, "X") == {}

    assign(link, "X", {"A": None, "B": None, "C": None})
    assert read(link, "X") == {"A": None, "B": None, "C": None}

    assign(graph, "g", {"A": {("A", "B"): None, "X": None}, "B": {("B", "B"): None, "X": None}, "C": {"X": None}, "X": {"A": None, "B": None, "C": None}})
    assert read(graph, "g") == {"A": {("A", "B"): None, "X": None}, "B": {("B", "B"): None, "X": None}, "C": {"X": None}, "X": {"A": None, "B": None, "C": None}}

    delete(node, "A")
    assert read(node, "A") is None

    delete(link, "X")
    assert read(link, "X") is None

    print("All tests pass!")
