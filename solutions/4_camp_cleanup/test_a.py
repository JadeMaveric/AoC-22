from typing import Callable, List, Tuple

Input = List[Tuple[Tuple[int, int]]]


def parse_input(filename: str) -> Input:
  inp = []

  with open(filename, 'r') as data:
    for line in data.readlines():
      section = []

      for boundary in line.strip().split(','):
        section.append([int(x) for x in boundary.split('-')])

      inp.append(section)

  return inp


def calculate_a(inp: Input) -> int:
  sum = 0

  for (a, b) in inp:
    # A contains B
    if a[0] >= b[0] and a[1] <= b[1]:
      sum += 1
    # B contains A
    elif b[0] >= a[0] and b[1] <= a[1]:
      sum += 1

  return sum


def calculate_b(inp: Input) -> int:
  sum = 0

  for (a, b) in inp:
    # A contains B's tail
    if a[0] <= b[1] and a[1] >= b[1]:
      sum += 1
    # B contains A's tail
    elif b[0] <= a[1] and b[1] >= a[1]:
      sum += 1

  return sum


def solve(filename: str, solver: Callable[[Input], int]):
  return solver(parse_input(filename))


class TestClass:

  def test_a(self):
    assert solve('input_eg.txt', calculate_a) == 2

  def test_b(self):
    assert solve('input_eg.txt', calculate_b) == 4


def main_a():
  out = solve('input.txt', calculate_a)
  print(f'Redundant pairs count = {out}')


def main_b():
  out = solve('input.txt', calculate_b)
  print(f'Overlapping pairs count = {out}')


if __name__ == '__main__':
  main_a()
  main_b()
