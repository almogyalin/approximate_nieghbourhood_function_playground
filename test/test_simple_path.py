import igraph as ig
from src.count_descendants_exact import count_descendants_exact
from src.count_descendants_hll import count_descendants_hll

def _make_simple_path():

    g = ig.Graph(directed=True, edges=[(0,1),(1,2),(2,3)])
    g.vs['is_detectable'] = True
    return g

def _make_expected():

    return [3,2,1,0]

def test_exact_counter():
    g = _make_simple_path()
    res = count_descendants_exact(g, "is_detectable")

    assert tuple(res) == tuple(_make_expected())

def test_hll_counter():

    g = _make_simple_path()
    res = count_descendants_hll(g, 'is_detectable')

    assert tuple(res) == tuple(_make_expected())
