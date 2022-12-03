from typing import List, Tuple
from functools import reduce


def parse_input_a(filename: str) -> List[Tuple[str, str]]:
  with open(filename, 'r') as data:
    parsed = []
    for line in data.readlines():
      line = line.strip()
      total = len(line) // 2
      parsed.append((line[:total], line[total:]))
    return parsed


def parse_input_b(filename: str) -> List[Tuple[str, str, str]]:
  parsed = []
  with open(filename, 'r') as data:
    state = []
    for line in data.readlines():
      state.append(line.strip())
      if len(state) == 3:
        parsed.append(state)
        state = []

  return parsed


def find_common(sacks: List[str]) -> str:
  s = None

  for items in sacks:
    s = s & set(items) if s else set(items)

  return s.pop() if s else None


def get_priority(char: str):
  if ord('a') <= ord(char) <= ord('z'):
    return ord(char) - ord('a') + 1
  elif ord('A') <= ord(char) <= ord('Z'):
    return ord(char) - ord('A') + 27
  else:
    raise ValueError('Must be a char between a-zA-Z')


def calculate(inp: List[Tuple[str, str]]) -> int:
  get_common_priority = lambda x: get_priority(find_common(x))
  return sum(get_common_priority(x) for x in inp)


class TestClass:

  def test_a(self):
    inp = parse_input_a('input_eg.txt')
    out = calculate(inp)
    assert out == 157

  def test_b(self):
    inp = parse_input_b('input_eg.txt')
    out = calculate(inp)
    assert out == 70


def main_a():
  inp = parse_input_a('input.txt')
  out = calculate(inp)
  print(f'Total priority = {out}')


def main_b():
  inp = parse_input_b('input.txt')
  out = calculate(inp)
  print(f'Group priority = {out}')


if __name__ == '__main__':
  main_a()
  main_b()
