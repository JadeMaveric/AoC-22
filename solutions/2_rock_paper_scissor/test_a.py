def parse_input(filename: str) -> (str, str):
  with open(filename, 'r') as data:
    lines = data.readlines()
    return [line.replace('\n', '').split(' ') for line in lines]


def get_score_a(opponent: str, player: str) -> int:
  move = {
    'X': 'rock',
    'Y': 'paper',
    'Z': 'scissor',
    'A': 'rock',
    'B': 'paper',
    'C': 'scissor'
  }

  opponent = move[opponent]
  player = move[player]

  sign_score = {'rock': 1, 'paper': 2, 'scissor': 3}
  base_score = sign_score[player]

  if player == opponent:
    base_score += 3
  elif player == 'rock' and opponent == 'scissor':
    base_score += 6
  elif player == 'paper' and opponent == 'rock':
    base_score += 6
  elif player == 'scissor' and opponent == 'paper':
    base_score += 6
  else:
    base_score += 0

  return base_score


def calculate_a(inp: (str, str)) -> int:
  score = 0

  for row in inp:
    score += get_score_a(row[0], row[1])

  return score


def get_score_b(opponent: str, outcome: str) -> int:
  move = {
    'X': 'lose',
    'Y': 'draw',
    'Z': 'win',
    'A': 'rock',
    'B': 'paper',
    'C': 'scissor'
  }

  opponent = move[opponent]
  outcome = move[outcome]

  outcome_score = {'win': 6, 'draw': 3, 'lose': 0}
  base_score = outcome_score[outcome]

  move_score = {
    'win': {
      'rock': 2,  #'paper'
      'paper': 3,  #'scissor'
      'scissor': 1,  #'rock'
    },
    'draw': {
      'rock': 1,
      'paper': 2,
      'scissor': 3
    },
    'lose': {
      'rock': 3,
      'paper': 1,
      'scissor': 2
    }
  }

  base_score += move_score[outcome][opponent]

  return base_score


def calculate_b(inp: (str, str)) -> int:
  score = 0

  for row in inp:
    score += get_score_b(row[0], row[1])

  return score


class TestClass:

  def test_a(self):
    inp = parse_input('input_eg.txt')
    out = calculate_a(inp)
    assert out == 15

  def test_b(self):
    inp = parse_input('input_eg.txt')
    out = calculate_b(inp)
    assert out == 12


def solve_a():
  inp = parse_input('input.txt')
  out = calculate_a(inp)
  print(f'ideal score = {out}')


def solve_b():
  inp = parse_input('input.txt')
  out = calculate_b(inp)
  print(f'actual score = {out}')


if __name__ == '__main__':
  solve_a()
  solve_b()
