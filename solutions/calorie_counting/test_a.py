# -- HELPERS --
def parse_input(inp: str):
  elf_calories = []

  for elf in inp.split('\n\n'):
    elf_calorie = [int(x) for x in elf.split('\n')]
    elf_calories.append(sum(elf_calorie))

  return elf_calories


def calculate_a(inp: str):
  elf_calories = parse_input(inp)
  return max(elf_calories)


def calculate_b(inp: str):
  elf_calories = parse_input(inp)
  return sum(sorted(elf_calories, reverse=True)[:3])


# -- TESTS --
class TestClass:

  def test_example_a(self):
    with open('input_eg.txt', 'r') as data:
      inp = data.read()
      out = 24000
      assert calculate_a(inp) == out

  def test_example_b(self):
    with open('input_eg.txt', 'r') as data:
      inp = data.read()
      out = 45000
      assert calculate_b(inp) == out


# -- RUNNERS --
def main_a():
  with open('input.txt', 'r') as data:
    max_cal = calculate_a(data.read())
    print(f'{max_cal=}')


def main_b():
  with open('input.txt', 'r') as data:
    top_3_cal = calculate_b(data.read())
    print(f'{top_3_cal=}')


if __name__ == '__main__':
  main_a()
  main_b()
