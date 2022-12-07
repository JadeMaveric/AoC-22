from typing import List, Tuple
import re

Input = Tuple[List[List[str]], List[List[int]]]

# ---- UTIL FUNCTIONS ---- #


def chunkify(arr: list, chunk_size: int):
  for i in range(0, len(arr), chunk_size):
    yield arr[i:i + chunk_size]


def filter_alphnumeric(s: str):
  s = re.sub('[^a-zA-Z]', '', s)
  return s.strip()


def not_empty(s: str):
  return s != ''


def format_stacks(arr: list):
  transponsed = (row for row in zip(*arr))
  filtered = (filter(not_empty, x) for x in transponsed)
  return list(list(x) for x in filtered)


def sanitize_instruction(instruction: str):
  instruction = instruction.replace("move", "")
  instruction = instruction.replace("from", "")
  instruction = instruction.replace("to", "")
  instruction = instruction.strip().split(" ")
  return [int(x) for x in filter(not_empty, instruction)]


# ---- START ----- #


def parse_input(filename: str) -> Input:
  stacks = []
  instructions = []

  stack_mode = True

  with open(filename, 'r') as data:
    lines = data.readlines()
    # Get the stacks
    for line in lines:
      line = line.replace('\n', '')

      if (line == ''):
        stack_mode = False
        continue

      if stack_mode:
        crates = list(chunkify(line, 4))  # ['[', 'A', ']', ' ']
        crates = [filter_alphnumeric(c) for c in crates]
        stacks.insert(0, crates)

      else:
        instructions.append(sanitize_instruction(line))

  stacks = format_stacks(stacks)

  return (stacks, instructions)


def calculate_a(inp: Input):
  (stacks, instructions) = inp

  def parse_instruction(stacks: list, instruction: list) -> list:
    quantity, from_idx, to_idx = instruction

    src_stack = stacks[from_idx - 1]
    dest_stack = stacks[to_idx - 1]

    for i in range(quantity):
      crate = src_stack.pop()
      dest_stack.append(crate)

  for instruction in instructions:
    parse_instruction(stacks, instruction)

  heads = []
  for stack in stacks:
    heads.append(stack[-1])

  return "".join(heads)


def calculate_b(inp: Input):
  (stacks, instructions) = inp

  def parse_instruction(stacks: list, instruction: list) -> list:
    quantity, from_idx, to_idx = instruction

    src_stack = stacks[from_idx - 1]
    dest_stack = stacks[to_idx - 1]

    crates = [src_stack.pop() for _ in range(quantity)]
    for crate in reversed(crates):
      dest_stack.append(crate)

  for instruction in instructions:
    parse_instruction(stacks, instruction)

  heads = []
  for stack in stacks:
    heads.append(stack[-1])

  return "".join(heads)


def solve(filename: str, solver):
  return solver(parse_input(filename))


class TestClass:

  def test_a(self):
    out = solve('input_eg.txt', calculate_a)
    assert out == 'CMZ'

  def test_b(self):
    out = solve('input_eg.txt', calculate_b)
    assert out == 'MCD'


def main_a():
  out = solve('input.txt', calculate_a)
  print(f"CrateMover 3000: {out}")


def main_b():
  out = solve('input.txt', calculate_b)
  print(f"CrateMover 3001: {out}")


if __name__ == '__main__':
  main_a()
  main_b()
