import networkx as nx
from types import MethodType

def count_nodes_and_edges(gs):
    nodes = sum(len(g.nodes) for g in gs)
    edges = sum(len(g.edges) for g in gs)
    return nodes, edges

def match_pair(g1, g2, method="edit_distance"):
    if method == "edit_distance":
        # Méthode 1 : Graph Edit Distance (GED)
        distance = nx.graph_edit_distance(g1, g2,timeout=60)
        print(f"Distance d'édition : {distance}")
        return distance

    elif method == "mcs":
        # Méthode 2 : Maximum Common Subgraph (MCS)
        ismags = nx.isomorphism.ISMAGS(g1, g2)
        # On extrait la taille du plus grand sous-graphe commun trouvé
        subgraphs = list(ismags.largest_common_subgraph())
        max_size = len(subgraphs[0]) if subgraphs else 0
        print(f"Taille du plus grand sous-graphe commun : {max_size}")
        return max_size

    elif method == "partial_iso":
        # Méthode 3 : Isomorphisme partiel (Heuristique)
        gm = nx.isomorphism.GraphMatcher(g1, g2)

        def partial_match(self):
            # Sécurisation de l'attribut max_core
            self.max_core = max(getattr(self, 'max_core', 0), len(self.core_1))
            self.current_iter += 1

            if len(self.core_1) >= len(self.G2) or self.current_iter >= self.max_iters:
                self.mapping = self.core_1.copy()
                yield self.mapping
            else:
                for G1_node, G2_node in self.candidate_pairs_iter():
                    if self.syntactic_feasibility(G1_node, G2_node):
                        if self.semantic_feasibility(G1_node, G2_node):
                            newstate = self.state.__class__(self, G1_node, G2_node)
                            yield from self.match()
                            newstate.restore()

        gm.match = MethodType(partial_match, gm)
        gm.max_iters = 100_000
        gm.current_iter = 0
        gm.max_core = 0
        
        is_iso = gm.subgraph_is_isomorphic()
        print(f"Isomorphisme partiel : {is_iso} | Taille du core max : {gm.max_core}")
        return gm.max_core

    else:
        raise ValueError("Méthode invalide. Choix : 'edit_distance', 'mcs', 'partial_iso'.")