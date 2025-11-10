from src.count_descendants_exact import count_descendants_exact
from src.count_descendants_hll import count_descendants_hll
import numpy as np
import igraph as ig

def _make_large_graph():

    np.random.seed(42)

    g = ig.Graph.Erdos_Renyi(n=1000, m=5000, directed=True)

    g.delete_edges([edge for edge in g.es if edge.target > edge.source])

    flags = [np.random.random() < 0.9 for _ in range(g.vcount())]

    g.vs['is_detectable'] = flags

    return g

def test_large_graph():

    g = _make_large_graph()

    exact = count_descendants_exact(g, 'is_detectable')

    approx = count_descendants_hll(g, 'is_detectable')

    rms = np.sqrt(sum((np.array(exact)-np.array(approx))**2)/len(exact))

    assert rms<0.2
