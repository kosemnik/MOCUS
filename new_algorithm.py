import networkx as nx

def get_cutset(tree):
    way = nx.algorithms.flow.max_flow_min_cost(tree.tn, s='SOURCE', t='STOCK')

    tree.tn.remove_node('SOURCE')
    tree.tn.remove_node('STOCK')

    for key in way:
        if key == 'SOURCE':
            continue
        for value in way[key]:
            if value == 'STOCK':
                continue
            if way[key][value] == 0:
                tree.tn.remove_edge(key, value)

    FT_reduce = tree.tn.subgraph(nx.shortest_path(tree.tn.to_undirected(), 'TOP'))

    result = []
    for edge in FT_reduce.edges:
        if edge[0] in tree.leaves:
            result.append(edge[0])

    return sorted(result)