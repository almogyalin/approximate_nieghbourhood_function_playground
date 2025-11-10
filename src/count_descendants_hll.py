from hyperloglog import HyperLogLog
import igraph as ig
import numpy as np

def count_descendants_hll(graph: ig.Graph, count_flag_name: str, hll_error_rate: float = 0.01) -> list[int]:
    n = graph.vcount()
    scc = graph.connected_components(mode='strong')
    scc_memberhsip = scc.membership
    n_sccs = max(scc_memberhsip) + 1

    scc_to_vertices: dict[int, list[int]] = {i:[] for i in range(n_sccs)}
    for vertex_id, scc_id in enumerate(scc_memberhsip):
        scc_to_vertices[scc_id].append(vertex_id)

    dag_edges = set()
    for edge in graph.es:
        src_scc = scc_memberhsip[edge.source]
        tgt_scc = scc_memberhsip[edge.target]
        if src_scc == tgt_scc:
            continue
        dag_edges.add((src_scc, tgt_scc))

    dag = ig.Graph(n=n_sccs, edges=list(dag_edges), directed=True)

    topo_order = dag.topological_sorting(mode='out')
    topo_order.reverse()

    hll_objects = [HyperLogLog(hll_error_rate) for _ in range(n_sccs)]

    true_flags = graph.vs[count_flag_name]

    for scc_id in topo_order:
        for vertex_id in scc_to_vertices[scc_id]:
            if true_flags[vertex_id]:
                hll_objects[scc_id].add(str(vertex_id))

        successors = dag.successors(scc_id)
        for succ_id in successors:
            hll_objects[scc_id].update(hll_objects[succ_id])

    dag_counts = np.array([len(hll) for hll in hll_objects])

    result = np.zeros(n, dtype=float)
    for scc_id in range(n_sccs):
        count = dag_counts[scc_id]

        true_count_in_scc = sum(true_flags[v] for v in scc_to_vertices[scc_id])

        for vertex_id in scc_to_vertices[scc_id]:
            result[vertex_id] = max(0, count - true_count_in_scc)

    return result
