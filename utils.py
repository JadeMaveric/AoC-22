import re


def chunkify(arr: list, chunk_size: int):
  for i in range(0, len(arr), chunk_size):
    yield arr[i:i + chunk_size]


def filter_alphnumeric(s: str):
  s = re.sub('[^a-zA-Z]', '', s)
  return s.strip()


def not_empty(s: str):
  return s != ''
