CRT_WIDTH = 40
CRT_HEIGHT = 6

class Util:

  @staticmethod
  def parse_input(filename: str) -> list:
    instructions = []

    with open(filename) as data:
      for line in data.readlines():
        if "addx" in line:
          instructions.append("noop")
        instructions.append(line.strip())

    return instructions

  @staticmethod
  def overlap(cycle: int, sprite: int) -> bool:
    cursor = cycle % CRT_WIDTH
    return abs(cursor - sprite) <= 1


class Solver:

  @staticmethod
  def solve_a(filename: str) -> int:
    inp = Util.parse_input(filename)

    target_cycles = [20, 60, 100, 140, 180, 220]
    X = 1
    strengths = []

    for clock, instruction in enumerate(inp):
      cycle = clock + 1

      if cycle in target_cycles:
        strengths.append(cycle * X)
      
      if instruction.startswith("addx"):
        V = instruction.split(" ")[1]
        X += int(V)

    return sum(strengths)

  @staticmethod
  def solve_b(filename: str) -> str:
    inp = Util.parse_input(filename)

    image = []

    X = 1

    for cycle in range(240):
      if Util.overlap(cycle, X):
        image.append("#")
      else:
        image.append(".")

      if cycle < len(inp):
        instruction = inp[cycle]
        if instruction.startswith("addx"):
          V = instruction.split(" ")[1]
          X += int(V)

    return ''.join(image)


class TestClass:

  def test_a(self):
    out = Solver.solve_a('input_eg.txt')
    assert out == 13140

  def test_b(self):
    out = Solver.solve_b('input_eg.txt')
    image = ''.join([
      "##..##..##..##..##..##..##..##..##..##..",
      "###...###...###...###...###...###...###.",
      "####....####....####....####....####....",
      "#####.....#####.....#####.....#####.....",
      "######......######......######......####",
      "#######.......#######.......#######....."
    ])
    assert out == image

if __name__ == '__main__':
  a = Solver.solve_a('input.txt')
  b = Solver.solve_b('input.txt')

  print(f"{a=}")

  print("b=")
  for x in range(CRT_HEIGHT):
    start = x * CRT_WIDTH
    end = start + CRT_WIDTH
    print(b[start:end])
