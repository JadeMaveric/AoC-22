from tqdm import tqdm
from operator import add, mul
from typing import Callable, List, Tuple
from dataclasses import dataclass


@dataclass
class Monkey:
    name: str
    inspect: Callable
    test: Callable
    items: list
    inspect_args: tuple
    test_args: tuple
    items_inspected: int = 0


class Util:
    @staticmethod
    def parse_input(filename: str) -> List[Monkey]:
        monkeys = []

        with open(filename) as data:
            monkey_lines: List[str] = []
            for line in data.readlines():
                if line.strip() == "":
                    monkey = Util.make_monkey(monkey_lines)
                    monkeys.append(monkey)
                    monkey_lines = []
                else:
                    monkey_lines.append(line)

        return monkeys

    @staticmethod
    def make_monkey(lines: list) -> Monkey:
        _items = lines[1].replace("Starting items:", "").strip()
        inspect_fn, inspect_args = Util.parse_operation(lines[2])
        test_fn, test_args = Util.parse_test(lines[3:])

        return Monkey(
            name=lines[0].replace(":", "").strip(),
            items=[int(item.strip()) for item in _items.split(", ")],
            inspect=inspect_fn,
            test=test_fn,
            inspect_args=inspect_args,
            test_args=test_args,
        )

    @staticmethod
    def parse_operation(line: str) -> Tuple[Callable, tuple]:
        line = line.replace("Operation: ", "").strip()

        operator = mul if "*" in line else add
        operand = line.split(" ")[-1]

        if operand.isdecimal():
            op_fn = lambda old: operator(old, int(operand))
        else:
            op_fn = lambda old: operator(old, old)

        op_symbol = "*" if "*" in line else "+"
        return op_fn, (op_symbol, operand)

    @staticmethod
    def parse_test(lines: list) -> Tuple[Callable, tuple]:
        dividend = int(lines[0].split(" ")[-1])
        true_monkey = int(lines[1].split(" ")[-1])
        false_monkey = int(lines[2].split(" ")[-1])

        def test_fn(num: int):
            modulo = num % dividend
            if modulo == 0:
                return true_monkey
            else:
                return false_monkey

        return test_fn, (dividend,)

    @staticmethod
    def identity(n: int) -> int:
        return n

    @staticmethod
    def product(l: list) -> int:
        acc = 1
        for n in l:
            acc *= n
        return acc


class Solver:
    @staticmethod
    def solve_a(filename: str) -> int:
        monkeys = Util.parse_input(filename)

        for round in tqdm(range(20), desc="Part A"):
            for midx, monkey in enumerate(monkeys):
                for iidx, item in enumerate(monkey.items):
                    monkey.items_inspected += 1

                    inspected_item = monkey.inspect(item) // 3
                    receiving_monkey = monkey.test(inspected_item)
                    monkeys[receiving_monkey].items.append(inspected_item)

                    if receiving_monkey == midx:
                        raise ValueError(
                            f"Receiving monkey is the same as throwing monkey {midx}"
                        )
                monkey.items = []

        monkey_items = sorted([m.items_inspected for m in monkeys])
        return monkey_items[-1] * monkey_items[-2]

    @staticmethod
    def solve_b(filename: str, rounds=10_000) -> int:
        monkeys = Util.parse_input(filename)
        modulo = Util.product([m.test_args[0] for m in monkeys])

        for round in tqdm(range(rounds), desc="Part B"):
            for midx, monkey in enumerate(monkeys):
                for iidx, item in enumerate(monkey.items):
                    monkey.items_inspected += 1

                    inspected_item = monkey.inspect(item) % modulo
                    receiving_monkey = monkey.test(inspected_item)
                    monkeys[receiving_monkey].items.append(inspected_item)

                    if receiving_monkey == midx:
                        raise ValueError(
                            f"Receiving monkey is the same as throwing monkey {midx}"
                        )
                monkey.items = []

        monkey_items = sorted([m.items_inspected for m in monkeys])
        return monkey_items[-1] * monkey_items[-2]


class TestClass:
    def test_a(self):
        out = Solver.solve_a("input_eg.txt")
        assert out == 10605

    def test_b(self):
        out = Solver.solve_b("input_eg.txt")
        assert out == 2713310158


if __name__ == "__main__":
    a = Solver.solve_a("input.txt")
    b = Solver.solve_b("input.txt", 10_000)

    print(f"{a=}")
    print(f"{b=}")
