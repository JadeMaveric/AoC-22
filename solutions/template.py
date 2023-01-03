
class Util:

  @staticmethod
  def parse_input(filename: str) -> list:
      ...


class Solver:

  @staticmethod
  def solve_a(filename: str) -> int:
      ...

  @staticmethod
  def solve_b(filename: str) -> int:
      ...


class TestClass:

  def test_a(self):
    out = Solver.solve_a('input_eg.txt')
    assert out == 21

  def test_b(self):
    out = Solver.solve_b('input_eg.txt')
    assert out == 8

if __name__ == '__main__':
  a = Solver.solve_a('input.txt')
  b = Solver.solve_b('input.txt')

  print("{a=}")
  print("{b=}")
