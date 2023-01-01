from dataclasses import dataclass, asdict


FILE = "file"
FOLDER = "folder"
TOTAL_MEMORY = 70_000_000
MIN_REQUIRED = 30_000_000


@dataclass
class Node:
  name: str = None
  type: str = None  # "file" | "folder"
  size: int = 0
  children: list = None
  parent = None

  def __init__(self,
               name=None,
               type=None,
               parent=None,
               size=None,
               children=None):
    self.name = name
    self.type = type
    self.parent = parent
    self.size = size
    self.children = children if children is not None else []

  def get_size(self):
    if self.size is not None:
      return self.size

    child_sizes = [child.get_size() for child in self.children]
    self.size = sum(child_sizes)
    return self.size

  def __eq__(self, other):
    return (self.name == other.name) and (self.type == other.type)

  def __repr__(self):
    return asdict(self).__repr__().replace("'", '"')


class FileSystem():
  root = None
  cwd = None

  def __init__(self):
    self.root = Node("/", FOLDER)
    self.cwd = self.root

  def __get_dir(self, dirname: str):
    if dirname == "/":
      return self.root

    elif dirname == ".":
      return self.cwd

    elif dirname == "..":
      if self.cwd.parent is None:
        raise ValueError(f"Cannot cd to parent of {self.cwd.name}")

      return self.cwd.parent

    else:
      target = Node(dirname, FOLDER)

      if target not in self.cwd.children:
        raise ValueError(f"directory {dirname} not found")

      child_idx = self.cwd.children.index(target)

      return self.cwd.children[child_idx]

  def cd(self, dirname: str = "/"):
    self.cwd = self.__get_dir(dirname)
    return self.cwd

  def ls(self, dirname: str = "."):
    dir = self.__get_dir(dirname)
    # pprint(dir, indent=2, depth=2)
    return dir

  def mk(self, name, type, size=None):
    node = Node(name, type, self.cwd, size)
    self.cwd.children.append(node)
    #self.cwd.size += node.get_size()
    return node


class Util:

  @staticmethod
  def parse_input(filename: str) -> FileSystem:
    fs = FileSystem()

    with open(filename, 'r') as data:
      for line in data.readlines():
        print(line)
        try:
          Util.parse_command(fs, line.strip())
        except AttributeError as e:
          print("name", fs.cwd.name)
          print("parent", fs.cwd.parent.name)
          print("command", line)
          print(fs.root)
          raise e

    return fs

  @staticmethod
  def parse_command(fs: FileSystem, command: str) -> None:
    # $ cd <dir> -> moving to directory
    if command.startswith("$ cd"):
      dir_name = command.split(' ')[-1]
      try:
        fs.cd(dir_name)
      except ValueError:
        fs.mk(dir_name, FOLDER)

    # $ ls -> print curr directory
    # we don't care about this line itself
    elif command.startswith("$ ls"):
      pass

    elif command.startswith("dir"):
      dir_name = command.split(' ')[-1]
      fs.mk(dir_name, FOLDER)

    else:
      (size, file_name) = command.split(' ')
      fs.mk(file_name, FILE, int(size))


class Solver:

  @staticmethod
  def solve_a(filename: str) -> int:
    fs = Util.parse_input(filename)
    fs.root.get_size()

    # Find directories with size <= 100_000
    threshold = 100_000
    stack = [fs.root]
    candidates = []

    while len(stack) > 0:
      cwd = stack.pop()
      
      if cwd.type != FOLDER:
        continue

      if cwd.get_size() < threshold:
        candidates.append(cwd)

      if cwd.children:
        stack.extend(cwd.children)

    return sum([dir.get_size() for dir in candidates])


  @staticmethod
  def solve_b(filename: str) -> int:
    fs = Util.parse_input(filename)

    used = fs.root.get_size()
    unused = TOTAL_MEMORY - used
    threshold = MIN_REQUIRED - unused

    if threshold <= 0:
      raise ValueError("There is enough memory, check input")

    # Find directories with size >= threshold
    stack = [fs.root]
    candidates = []

    while len(stack) > 0:
      cwd = stack.pop()
      
      if cwd.type != FOLDER:
        continue

      if cwd.get_size() >= threshold:
        candidates.append(cwd)

      if cwd.children:
        stack.extend(cwd.children)

    return min([dir.get_size() for dir in candidates])

class TestClass:

  def test_a(self):
    out = Solver.solve_a('input_eg.txt')
    assert out == 95437

  def test_b(self):
    out = Solver.solve_b('input_eg.txt')
    assert out == 24933642

if __name__ == '__main__':
  a = Solver.solve_a('input.txt')
  b = Solver.solve_b('input.txt')

  print(f'{a=}, {b=}')
