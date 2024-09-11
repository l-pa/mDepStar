import math
from collections import defaultdict
from .Network import Network

class mDepStar:
    def __init__(
        self, graph: Network, dependency: float | list[tuple[str, str]] | None = None
    ) -> None:
        self._G: Network = graph
        self._weighted_degree_matrix: dict[str, float] = {}
        self._dependency_cache: dict[tuple[str, str], float] = {}

        self._dependency_matrix: dict[str, dict[str, float]] | None = None
        self._mDep_network_dict: dict[str, dict[str, float]] | None = None
        self._dependency_threshold: float | None = None

        self._calc_dependency_matrix()
        if isinstance(dependency, float):
            print(f"Dependency is set to {dependency}")
            self._dependency_threshold = dependency

        elif isinstance(dependency, list):
            self._dependency_threshold = self._estimate_dependency(dependency)

    @property
    def dependency_threshold(self):
        if self._dependency_threshold is None:
            self._dependency_threshold = round(
                self._estimate_dependency(self._G.edges()), 3
            )
        return self._dependency_threshold

    @dependency_threshold.setter
    def dependency_threshold(self, value):
        self._dependency_threshold = value

    def get_dependency(self, A: str, B: str) -> float:
        """Get dependency between two nodes

        Args:
            A (str): node A
            B (str): node B

        Returns:
            float: dependency
        """

        if self._dependency_matrix is not None:
            if self._G.edge_exists(A, B):
                return self._dependency_matrix[A][B]
            else:
                return self._dependency(A, B)
        else:
            raise Exception("Dependency matrix is None")

    def _avg_dependency(self, edges: list[tuple[str, str]]):

        d = 0

        for e in edges:
            d1 = self.get_dependency(e[0], e[1])
            d2 = self.get_dependency(e[1], e[0])

            d += (d1 + d2) / 2

        return 0 if d == 0 else d / len(edges)

    def _estimate_dependency(self, edges: list[tuple[str, str]] | None = None) -> float:
        if edges is None:
            edges = self._G.edges()

        depWeightedSum = 0
        depWeights = 0

        for e in edges:
            d1 = self.get_dependency(e[0], e[1])
            d2 = self.get_dependency(e[1], e[0])

            min_of_dep = min(d1, d2)

            depWeightedSum += min_of_dep * ((d1 + d2) / 2)
            depWeights += min_of_dep

        if depWeights == 0:
            return 1

        return depWeightedSum / depWeights / 2

    def get_node_deps(self, node: str):
        """Get the number of mutual dependencies, no dependencies, node is dependent on neighbor, neighbor is dependent on node.

        Args:
            node (str): node

        Returns:
            _type_: Two way dep;No dep;Node on neighbor;Neighbor on node
        """
        node_is_dep_on = 0
        neighbors_are_dep_on_node = 0
        mutual_dep = 0
        no_dep = 0

        if self._dependency_matrix is not None:
            for neighbor in self._G.neighbors(node):
                d1 = self._dependency_matrix[node][neighbor]
                d2 = self._dependency_matrix[neighbor][node]

                if d1 < self.dependency_threshold and d2 < self.dependency_threshold:
                    no_dep += 1
                elif mDepStar._is_greater_or_equal(
                    d1, self.dependency_threshold, 6
                ) and mDepStar._is_greater_or_equal(d2, self.dependency_threshold, 6):
                    mutual_dep += 1
                elif mDepStar._is_greater_or_equal(d1, self.dependency_threshold, 6):
                    node_is_dep_on += 1
                elif mDepStar._is_greater_or_equal(d2, self.dependency_threshold, 6):
                    neighbors_are_dep_on_node += 1
        return mutual_dep, no_dep, node_is_dep_on, neighbors_are_dep_on_node

    def _weight(self, x: str, y: str) -> float:
        if self._G.weighted:
            return self._G.weight(x, y)
        else:
            return 1

    def _r(self, x: str, common_neighbor: str, y: str) -> float:
        denom = self._weight(x, common_neighbor) + self._weight(common_neighbor, y)

        return (
            0
            if denom == 0
            else self._weight(common_neighbor, y)
            / (self._weight(x, common_neighbor) + self._weight(common_neighbor, y))
        )

    def _weighted_degree(self, x: str) -> float:

        neighbors_sum = 0.0

        if self._weighted_degree_matrix.get(x, None) is None:

            for node in self._G.neighbors(x):
                neighbors_sum += self._weight(x, node)

            self._weighted_degree_matrix[x] = neighbors_sum

        return self._weighted_degree_matrix[x]

    def _dependency(self, x: str, y: str) -> float:

        common_sum = 0.0

        for node in self._G.common_neighbors(x, y):
            common_sum += self._weight(x, node) * self._r(x, node, y)

        denom = self._weighted_degree(x)

        return (
            0
            if denom == 0
            else (self._weight(x, y) + common_sum) / (self._weighted_degree(x))
        )

    def _calc_dependency_matrix(self) -> dict[str, dict[str, float]] | None:
        dep_matrix: dict = defaultdict(dict)

        for edge in self._G.edges():
            i: str
            j: str
            i = edge[0]
            j = edge[1]

            d1 = self._dependency(i, j)
            d2 = self._dependency(j, i)

            dep_matrix[i][j] = d1
            dep_matrix[j][i] = d2

        self._dependency_matrix = dep_matrix

    def _get_mDep_network(self):

        if self._dependency_matrix is None:
            raise Exception("Dependency matrix is empty")

        mDep_network: dict = defaultdict(dict)

        for nodeA in self._dependency_matrix.keys():
            for nodeB in self._dependency_matrix[nodeA].keys():
                d1 = self._dependency_matrix[nodeA][nodeB]
                d2 = self._dependency_matrix[nodeB][nodeA]
                if mDepStar._is_greater_or_equal(
                    d1, self.dependency_threshold, 6
                ) and mDepStar._is_greater_or_equal(d2, self.dependency_threshold, 6):
                    mDep_network[nodeA][nodeB] = d1
                    mDep_network[nodeB][nodeA] = d2

        return mDep_network
    
    def _check_condition(self, node: str, mutual_dep_neighbors: set[str]):
        res = set()
        for neigh in list(mutual_dep_neighbors):
                if (
                    mDepStar._is_greater_or_equal(
                        self.get_dependency(neigh, node), 2 * self.dependency_threshold
                    )
                ) or (
                    mDepStar._is_greater_or_equal(
                        self.get_dependency(node, neigh), 2 * self.dependency_threshold
                    )
                ):
                    res.add(neigh)
        return res


    def get_complexes(self, node: str | None = None) -> set[frozenset[str]]:
        """Get the complexes in the network based on dependency values and threshold value.
        Raises:
            Exception: Dependency matrix is empty

        Returns:
            set[frozenset[str]]: Set of predicted complexes
        """

        if self._dependency_matrix is None:
            raise Exception("Dependency matrix is empty")

        complexes: set[frozenset[str]] = set()
        mDep_network = self.get_mDep_network()

        if node is not None and node in mDep_network.nodes():
            c = set(mDep_network.neighbors(node))
            return set([frozenset([node]).union(self._check_condition(node, c))])

        for n in mDep_network.nodes():
            c = set(mDep_network.neighbors(n))
            res = set([n]).union(self._check_condition(n, c))
            if len(res) >= 3:
                complexes.add(frozenset(res))
        return complexes

    def _get_mDep_network_edges(self, edges: list[tuple[str, str]]):
        if self._dependency_matrix is None:
            raise Exception("Dependency matrix is empty")

        mDep_network: dict = defaultdict(dict)

        for edge in edges:
            nodeA = edge[0]
            nodeB = edge[1]

            d1 = self._dependency_matrix[nodeA][nodeB]
            d2 = self._dependency_matrix[nodeB][nodeA]
            if mDepStar._is_greater_or_equal(
                d1, self.dependency_threshold, 6
            ) and mDepStar._is_greater_or_equal(d2, self.dependency_threshold, 6):
                mDep_network[nodeA][nodeB] = d1
                mDep_network[nodeB][nodeA] = d2

        return mDep_network

    def edge_dependency(self, edge: tuple[str, str]) -> tuple[float, float]:
        if self._dependency_matrix is None:
            self._calc_dependency_matrix()

        return (self._dependency_matrix[edge[0]][edge[1]], self._dependency_matrix[edge[1]][edge[0]])  # type: ignore

    def get_mDep_network(self) -> Network:
        if self._mDep_network_dict is None:
            self._mDep_network_dict = self._get_mDep_network()

        G = Network()

        for nodeA in self._mDep_network_dict.keys():
            for nodeB in self._mDep_network_dict[nodeA].keys():
                G.add_edge(nodeA, nodeB, 1)

        return G

    def get_mDep_network_edges(self, edges: list[tuple[str, str]]) -> Network:
        """Construct a new network from edges that are dependent on each other, but use dependency values from the whole network.

        Args:
            edges (list[tuple[str,str]]): edges from which a new mDep network is created

        Returns:
            Network: a new mDep network
        """

        _mDep_network_dict = self._get_mDep_network_edges(edges)

        G = Network()

        for nodeA in _mDep_network_dict.keys():
            for nodeB in _mDep_network_dict[nodeA].keys():
                G.add_edge(nodeA, nodeB, 1)

        return G

    def export(
        self, lst: set[frozenset[str]], file_name: str, delimiter: str = " "
    ) -> None:
        """
        Save complexes to a file, each complex is on a separate line.
        """
        with open(file_name, "w") as f:
            for i in list(lst):
                f.write(f"{delimiter.join(i)}\n")

    def export_mDep_network(self, file_name: str):
        """
        Save mDep network to a file.
        """
        res = []
        tmp = set()

        if self._mDep_network_dict is not None:
            for i in self._mDep_network_dict.keys():
                for j in self._mDep_network_dict[i].keys():
                    tmp.add(frozenset([i, j]))

            for i in tmp:
                a = list(i)
                a.append(self._G.get_edge_weight(a[0], a[1]))
                res.append(a)
            print(f"Mdep networks saved as {file_name}")
            with open(file_name, "w") as f:
                for i in res:
                    f.write(f"{i[0]};{i[1]};{i[2]}\n")

    @staticmethod
    def _is_greater_or_equal(x: float, y: float, decimals=6) -> bool:
        """Rounding precision errors"""
        if x <= y:
            return math.isclose(x, y, rel_tol=pow(10.0, -decimals))

        return True
