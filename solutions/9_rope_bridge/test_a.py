def sign(a: int) -> int:
  if a > 0:
    return 1
  elif a < 0:
    return -1
  else:
    return 0

class Util:

  @staticmethod
  def parse_input(filename: str) -> list:
      instructions = []

      with open(filename) as data:
        for line in data.readlines():
          direction, step = line.strip().split(' ')
          instructions.append((direction, int(step)))

      return instructions

  @staticmethod
  def update_head(head_x: int, head_y: int, direction: str) -> tuple:
    if direction == 'L':
      return head_x - 1, head_y
    elif direction == 'R':
      return head_x + 1, head_y
    elif direction == 'U':
      return head_x, head_y + 1
    elif direction == 'D':
      return head_x, head_y - 1
    else:
      raise ValueError(f"`direction` must be one of U/D/L/R, found {direction}")

  @staticmethod
  def update_tail(head_x: int, head_y: int,
                  tail_x: int, tail_y: int) -> tuple:
    # the head (H) and tail (T) must always be touching
    # (diagonally adjacent and even overlapping both count as touching)
    if abs(head_x - tail_x) <= 1 and abs(head_y - tail_y) <= 1:
      return tail_x, tail_y
    
    # If the head is ever two steps directly up, down, left, or right from the tail,
    # the tail must also move one step in that direction so it remains close enough
    # Otherwise, if the head and tail aren't touching and aren't in the same row or column,
    # the tail always moves one step diagonally to keep up:
    # This can be simplified to the following
    else:
      return (tail_x + sign(head_x - tail_x)), (tail_y + sign(head_y - tail_y))


class Solver:

  @staticmethod
  def solve_a(filename: str) -> int:
    inp = Util.parse_input(filename)

    head = (0, 0)
    tail = (0, 0)

    tail_pos = set()
    tail_pos.add(tail)

    for (direction, step) in inp:
      for _ in range(step):
        head = Util.update_head(head[0], head[1], direction)
        tail = Util.update_tail(head[0], head[1], tail[0], tail[1])
        tail_pos.add(tail)

    return len(tail_pos)


  @staticmethod
  def solve_b(filename: str) -> int:
    inp = Util.parse_input(filename)

    rope = [(0,0)] * 10

    tail_pos = set()
    tail_pos.add(rope[-1])

    for (direction, step) in inp:
      for _ in range(step):
        rope[0] = Util.update_head(rope[0][0], rope[0][1], direction)

        for idx, tail in enumerate(rope[1:]):
          head = rope[idx]
          rope[idx+1] = Util.update_tail(head[0], head[1], tail[0], tail[1])

        tail_pos.add(rope[-1])

    return len(tail_pos)


class TestClass:

  def test_a(self):
    out = Solver.solve_a('input_eg.txt')
    assert out == 13

  def test_b(self):
    out = Solver.solve_b('input_eg.txt')
    assert out == 1

  def test_b_2(self):
    out = Solver.solve_b('input_eg_2.txt')
    assert out == 36

if __name__ == '__main__':
  a = Solver.solve_a('input.txt')
  b = Solver.solve_b('input.txt')
  print(f"{a=}")
  print(f"{b=}")
