from dataclasses import dataclass

@dataclass
class Tree:
  height: int
  visible: bool

class Util:

  @staticmethod
  def parse_input(filename: str) -> list:
    rows = []

    with open(filename) as data:
      for line in data.readlines():
        col = [int(n) for n in line.strip()]
        rows.append(col)

    return rows

  @staticmethod
  def get_visible_indices(row: list) -> list:
    visible_indices = []
    unseen = []

    visible_threshold = row[0]


    # Check left to right
    for idx, cell in enumerate(row):
      unseen = [n for n in unseen if row[n] > cell]

      if idx == 0:
        visible_indices.append(idx)
      
      elif cell > visible_threshold:
        visible_threshold = cell
        visible_indices.append(idx)

      else:
        unseen.append(idx)

    # Check right to left (unseen)
    for idx in unseen[::-1]:
      cell = row[idx]

      if idx == len(row) - 1:
        visible_threshold = cell
        visible_indices.append(idx)

      elif cell > visible_threshold:
        visible_threshold = cell
        visible_indices.append(idx)

    return visible_indices


  @staticmethod
  def get_scenic_scores(row):
    score = []

    for idx, cell in enumerate(row):
      curr_score = 0

      for curr in row[idx+1:]:
        curr_score += 1
        if curr >= cell:
          break

      score.append(curr_score)

    return score



class Solver:

  @staticmethod
  def solve_a(filename: str) -> int:
    grid = Util.parse_input(filename)

    visible = set()

    for idx, row in enumerate(grid):
      row_idx = Util.get_visible_indices(row)
      visible = visible.union([(idx, idr) for idr in row_idx])

    transposed = list(zip(*grid))
    for idx, col in enumerate(transposed):
      col_idx = Util.get_visible_indices(col)
      visible = visible.union([(idc, idx) for idc in col_idx])

    return len(visible)

  @staticmethod
  def solve_b(filename: str) -> int:
    inp = Util.parse_input(filename)
    scores = [[1] * len(row) for row in inp]

    # Rows L -> R
    for idx, row in enumerate(inp):
      row_score = Util.get_scenic_scores(row)
      rev_row_score = Util.get_scenic_scores(row[::-1])[::-1]
      scores[idx] = [a*b*c for a,b,c in zip(scores[idx], row_score, rev_row_score)]

    inp_t = list(zip(*inp))
    scores_t = list(zip(*scores))
    # Col L -> R
    for idx, row in enumerate(inp_t):
      row_score = Util.get_scenic_scores(row)
      rev_row_score = Util.get_scenic_scores(row[::-1])[::-1]
      scores_t[idx] = [a*b*c for a,b,c in zip(scores_t[idx], row_score, rev_row_score)]

    final_scores = list(zip(*scores_t))

    return max([max(row) for row in final_scores])


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
  print(f"{a=}")
  print(f"{b=}")

