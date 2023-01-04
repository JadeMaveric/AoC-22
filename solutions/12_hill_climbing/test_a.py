import networkx as nx


class Util:
    @staticmethod
    def parse_input(filename: str) -> tuple:
        grid = []

        with open(filename) as data:
            grid = [[ch for ch in line.strip()] for line in data.readlines()]

        return Util.build_graph(grid)

    @staticmethod
    def build_graph(grid: list) -> tuple:
        G = nx.DiGraph()
        start = None
        end = None

        # Add edges
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                node_c, is_start, is_end = Util.get_node(grid, row, col)
                node_n, _, _ = Util.get_node(grid, row - 1, col)
                node_e, _, _ = Util.get_node(grid, row, col + 1)
                node_w, _, _ = Util.get_node(grid, row, col - 1)
                node_s, _, _ = Util.get_node(grid, row + 1, col)

                if node_c is None:
                    raise ValueError(f"Current node cannot be none: {row=} {col=}")
                elif is_start:
                    start = node_c
                elif is_end:
                    end = node_c

                if node_n is not None and ord(node_n[2]) - ord(node_c[2]) <= 1:
                    G.add_edge(node_c, node_n)
                if node_e is not None and ord(node_e[2]) - ord(node_c[2]) <= 1:
                    G.add_edge(node_c, node_e)
                if node_w is not None and ord(node_w[2]) - ord(node_c[2]) <= 1:
                    G.add_edge(node_c, node_w)
                if node_s is not None and ord(node_s[2]) - ord(node_c[2]) <= 1:
                    G.add_edge(node_c, node_s)

        return G, start, end

    @staticmethod
    def get_node(grid: list, row: int, col: int) -> tuple:
        if row < 0 or col < 0:
            return None, False, False

        elif row >= len(grid) or col >= len(grid[row]):
            return None, False, False

        else:
            height = grid[row][col]
            is_start = False
            is_end = False

            if height == "S":
                height = "a"
                is_start = True
            if height == "E":
                height = "z"
                is_end = True

            return (row, col, height), is_start, is_end


class Solver:
    @staticmethod
    def solve_a(filename: str) -> int:
        G, start, end = Util.parse_input(filename)
        return nx.shortest_path_length(G, start, end)

    @staticmethod
    def solve_b(filename: str) -> int:
        G, start, end = Util.parse_input(filename)
        shortest_path_length = nx.shortest_path_length(G, start, end)

        candidate_starts = [n for n in G.nodes() if n[2] == "a" and n != start]

        for s in candidate_starts:
            try:
                shortest_path_length = min(
                    shortest_path_length, nx.shortest_path_length(G, s, end)
                )
            except nx.exception.NetworkXNoPath:
                continue

        return shortest_path_length


class TestClass:
    def test_a(self):
        out = Solver.solve_a("input_eg.txt")
        assert out == 31

    def test_b(self):
        out = Solver.solve_b("input_eg.txt")
        assert out == 29


if __name__ == "__main__":
    a = Solver.solve_a("input.txt")
    b = Solver.solve_b("input.txt")

    print(f"{a=}")
    print(f"{b=}")
