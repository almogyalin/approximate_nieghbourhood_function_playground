import igraph as ig
import numpy as np
from tqdm import tqdm

def count_descendants_exact(graph: ig.Graph, count_flag_name: str) -> list[int]:
    neighbourhoods = graph.neighborhood(graph.vs, mode='out', order=graph.vcount(), mindist=1)
    return [sum(graph.vs[neighbourhood][count_flag_name]) for neighbourhood in neighbourhoods]

def count_descendants_chunked(graph: ig.Graph, count_flag_name: str, chunks: int = 20) -> list[int]:
    chunked_arrays = np.array_split(np.array(range(graph.vcount())), chunks)
    res = []
    for chunk in tqdm(chunked_arrays):
        neighbourhoods = graph.neighborhood(chunk, mode='out', order=graph.vcount(), mindist=1)
        res += [sum(graph.vs[neighbourhood][count_flag_name]) for neighbourhood in neighbourhoods]
    return res
