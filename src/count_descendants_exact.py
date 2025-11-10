import igraph as ig

def count_descendants_exact(graph: ig.Graph, count_flag_name: str) -> list[int]:
    neighbourhoods = graph.neighborhood(graph.vs, mode='out', order=graph.vcount())
    return [sum(graph.vs[neighbourhood][count_flag_name]) for neighbourhood in neighbourhoods]
