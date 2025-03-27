from collections import defaultdict
import networkx as nx
from collections import deque

class Network(object):

    def __init__(self) -> None:
        self._edges = []
        self._nodes = set()

        self._network: dict[str, dict[str, float]
                            ] = defaultdict(lambda: defaultdict(float))

        self._weighted = False
        self._neighbors = defaultdict(set)
        self._file_name: str = None

    def __str__(self) -> str:
        return f"{len(self._nodes)} nodes - {len(self._edges)} edges - {hex(id(self))}"

    def read_file(self, file_name: str, sep=';', weighted=False):

        self._file_name = file_name
        self._weighted = weighted

        if len(self.edges()) > 0:
            raise Exception("Edges already exists")

        f = open(file_name, "r")

        if weighted:
            for l in f.read().splitlines():
                node = l.split(sep)
                self.add_edge(node[0], node[1], float(node[2].replace(',', '.')))

        else:
            for l in f.read().splitlines():
                node = l.split(sep)
                self.add_edge(node[0], node[1], 1)

    @property
    def weighted(self):
        return self._weighted

    @weighted.setter
    def weighted(self, value):
        self._weighted = value

    @property
    def density(self):
        if len(self.nodes()) == 0:
            return 0

        if len(self.nodes()) == 1:
            return 1

        return (2 * len(self._edges)) / (len(self.nodes()) * (len(self.nodes()) - 1))

    @property
    def avg_degree(self):

        n = 0

        for i in self.nodes():
            n += self.degree(i)

        if len(self.nodes()) == 0:
            return 0

        return n / len(self.nodes())
    
    def add_edge(self, a: str, b: str, weight: float):
        if not self.edge_exists(a, b) and not self.edge_exists(b, a) and a != b:


            self._network[a][b] = weight
            self._network[b][a] = weight

            self._neighbors[a].add(b)
            self._neighbors[b].add(a)

            self._edges.append((a, b))
            self.add_node(a)
            self.add_node(b)

    def remove_edge(self, a: str, b: str):
        if self.edge_exists(a, b):
            if len(self.neighbors(a)) == 1:
                self._remove_node(a)

            if len(self.neighbors(b)) == 1:
                self._remove_node(b)
        
            del self._network[a][b]
            del self._network[b][a]

            self._neighbors[a].remove(b)
            self._neighbors[b].remove(a)

            try:
                self._edges.remove((a, b))
                self._edges.remove((b,a))
            except Exception as e:
                pass

    def edge_exists(self, a: str, b: str) -> bool:
        if b in self.neighbors(a):
            return True
        return False

    def _remove_node(self, node: str):
        self._nodes.remove(node)

    def degree(self, node: str) -> int:
        return len(self.neighbors(node))
    
    def clustering_coeficient_node(self, node: str):
        nodes_around = self.neighbors_depth(set([node]), 0, 1)
        nodes_around.remove(node)

        degree = self.degree(node)

        if degree == 1:
            return 0

        return (2 * len(self.induced_subgraph(nodes_around).edges())) / (degree * (degree - 1))

    def clustering_coeficient(self):
        if len(self.nodes()) == 0:
            return 0
        else:
            return sum([self.clustering_coeficient_node(i) for i in self.nodes()]) / len(self.nodes())

    def add_node(self, node: str):
        self._nodes.add(node)

    def get_edge_weight(self, a: str, b: str) -> float:
        return self._network[a][b]

    def neighbors(self, node: str) -> set[str]:
        return self._neighbors[node]

    def common_neighbors(self, x: str, y: str) -> frozenset[str]:
        return self.neighbors(x).intersection(self.neighbors(y))

    def weight(self, nodeA: str, nodeB: str) -> float:
        return self._network[nodeA][nodeB]

    def edges(self) -> list[tuple[str, str]]:
        return self._edges

    def nodes(self) -> set[str]:
        return self._nodes

    def file_name(self) -> str:
        return self._file_name

    def induced_subgraph(self, nodes: set[str]):

        a = Network()

        for node in nodes:
            if node not in self._neighbors:
                continue  # Skip if the node has no edges
            
            for neighbor in self._neighbors[node]:
                if neighbor in nodes:
                    a.add_edge(node, neighbor, self.get_edge_weight(node, neighbor))

        return a

    def neighbors_depth(self, result_nodes: set[str], current_depth: int, max_depth: int) -> set[str]:
        res = set(result_nodes)
        temp_neighbors = set()
        
        for node in result_nodes:
            neighbors = self.neighbors(node) 
            temp_neighbors.update(neighbors)
        
        res.update(temp_neighbors)
        return res
        
    def to_networkx(self) -> nx.Graph:
        
        tmp_G : nx.Graph = nx.Graph()
        for e in self.edges():
            tmp_G.add_edge(e[0], e[1], weight=self.weight(e[0], e[1]), label = e[0] +'-'+ e[1])

        return tmp_G

    def save_to_file(self, file_name:str):
        f = open(file_name, mode='w')

        for i in self._edges:
            f.write(';'.join(i) + ';' + str(self.get_edge_weight(i[0], i[1])) + '\n')

        f.close()

