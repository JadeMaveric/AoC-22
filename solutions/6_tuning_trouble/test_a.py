class Util:

  @staticmethod
  def parse_input(filename: str) -> str:
    with open(filename) as data:
      return data.read()


class Solver:

  @staticmethod
  def find_marker(inp: str, unique_count: int) -> int:
    for idx in range(len(inp) - unique_count):
      seq = inp[idx:idx + unique_count]
      if len(set(seq)) == unique_count:
        return idx + unique_count
    else:
      return None

  @staticmethod
  def solve_a(inp: str) -> int:
    return Solver.find_marker(inp, 4)

  @staticmethod
  def solve_b(inp: str) -> int:
    return Solver.find_marker(inp, 14)


class TestClass:

  def test_a(self):

    tests = [
      ('input_eg_0.txt', 7),
      ('input_eg_1.txt', 5),
      ('input_eg_2.txt', 6),
      ('input_eg_3.txt', 10),
      ('input_eg_4.txt', 11),
    ]

    for (filename, expected) in tests:
      inp = Util.parse_input(filename)
      out = Solver.solve_a(inp)
      assert out == expected

  def test_b(self):

    tests = [
      ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 19),
      ('bvwbjplbgvbhsrlpgdmjqwftvncz', 23),
      ('nppdvjthqldpwncqszvftbrmjlhg', 23),
      ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 29),
      ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 26),
    ]

    for (inp, expected) in tests:
      #inp = Util.parse_input(filename)
      out = Solver.solve_b(inp)
      assert out == expected


if __name__ == '__main__':
  inp = Util.parse_input('input.txt')
  out = Solver.solve_a(inp)
  print(f'packet: {out}')

  out = Solver.solve_b(inp)
  print(f'message: {out}')
