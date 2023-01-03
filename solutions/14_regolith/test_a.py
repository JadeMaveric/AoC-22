SAND_SPAWN_POINT = (500, 0)
FLOOR_OFFSET = 2


class Util:
    @staticmethod
    def parse_input(filename: str) -> list:
        rocks = []

        with open(filename) as data:
            for line in data.readlines():
                temp0 = line.strip().split(" -> ")
                temp1 = [t.split(",") for t in temp0]
                temp2 = [(int(a), int(b)) for a, b in temp1]
                rocks.append(temp2)

        return rocks

    @staticmethod
    def build_grid(inp: list, part_b=False) -> tuple:
        all_points = [point for points in inp for point in points]

        min_x = min([c[0] for c in all_points])
        max_x = max([c[0] for c in all_points])
        max_y = max([c[1] for c in all_points])

        grid = [["."] * (max_x + 2) for _ in range(max_y + 1)]

        if part_b:
            grid.append(["."] * (max_x + 2))
            grid.append(["#"] * (max_x + 2))
            grid.append(["."] * (max_x + 2))

        for path in inp:
            for start, end in zip(path[:-1], path[1:]):  # segments of the path
                Util.draw_line(grid, start, end)

        if part_b:
            for col in grid:
                col[max_y + FLOOR_OFFSET] = "#"

        return grid, min_x

    @staticmethod
    def draw_line(grid, start, end):
        x0, y0 = start
        x1, y1 = end

        if x0 == x1:
            _range = range(y0, y1 + 1) if y0 < y1 else range(y1, y0 + 1)
            for y in _range:
                grid[y][x0] = "#"

        if y0 == y1:
            _range = range(x0, x1 + 1) if x0 < x1 else range(x1, x0 + 1)
            for x in _range:
                grid[y0][x] = "#"

    @staticmethod
    def update_grid(grid: list, sand_point: tuple) -> tuple:
        x, y = sand_point

        # If the sand is at the edge, it cannot rest
        if y + 1 == len(grid):
            return grid, sand_point, False

        # If the sand can move down, it should
        if grid[y + 1][x] == ".":
            sand_point = (x, y + 1)
            return grid, sand_point, True

        # sand will then try to move down-left
        if x > 0 and grid[y + 1][x - 1] == ".":
            sand_point = (x - 1, y + 1)
            return grid, sand_point, True

        # sand will then try to move down-right
        if x + 1 == len(grid[y + 1]):
            block = "#" if grid[y + 1][x] == "#" else "."
            grid[y + 1].append(block)

        if grid[y + 1][x + 1] == ".":
            sand_point = (x + 1, y + 1)
            return grid, sand_point, True

        # finally, sand will then rest
        else:
            grid[y][x] = "o"
            source_blocked = sand_point == SAND_SPAWN_POINT
            return grid, SAND_SPAWN_POINT, not source_blocked

    @staticmethod
    def print_grid(grid: list, min_x=0, prefix="grid="):
        print(prefix)
        for row in grid:
            print("".join(row[min_x - 30 :]))


class Solver:
    @staticmethod
    def solve(filename: str, part_b=False) -> int:
        inp = Util.parse_input(filename)
        grid, min_x = Util.build_grid(inp, part_b)

        Util.print_grid(grid, min_x)

        running = True
        sand_count = 0
        sand_pos = SAND_SPAWN_POINT

        while running:
            grid, sand_pos, running = Util.update_grid(grid, sand_pos)
            if sand_pos == SAND_SPAWN_POINT:
                sand_count += 1
                # Util.print_grid(grid, min_x)
                print(f"{sand_count=}")

        Util.print_grid(grid, min_x)
        return sand_count

    @staticmethod
    def solve_a(filename: str) -> int:
        return Solver.solve(filename, False)

    @staticmethod
    def solve_b(filename: str) -> int:
        return Solver.solve(filename, True)


class TestClass:
    def test_a(self):
        out = Solver.solve_a("input_eg.txt")
        assert out == 24

    def test_b(self):
        out = Solver.solve_b("input_eg.txt")
        assert out == 93


if __name__ == "__main__":
    a = Solver.solve_a("input.txt")
    b = Solver.solve_b("input.txt")

    print(f"{a=}")
    print(f"{b=}")
