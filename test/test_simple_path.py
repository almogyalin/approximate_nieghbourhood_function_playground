import igraph as ig
from src.count_descendants_exact import count_descendants_exact

def _make_simple_path():

    g = ig.Graph(directed=True, edges=[(0,1),(1,2),(2,3)])
    g.vs['is_detectable'] = True
    return g

def test_exact_counter():
    g = _make_simple_path()
    res = count_descendants_exact(g, "is_detectable")

    expected = [4,3,2,1]
    assert tuple(res) == tuple(expected)
