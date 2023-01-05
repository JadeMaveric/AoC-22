from functools import cmp_to_key, reduce
import json


class Util:
    @staticmethod
    def parse_input(filename: str) -> list:
        packet_pairs = []

        with open(filename) as data:
            pair = []
            for line in data.readlines():
                if line.strip() == "":
                    packet_pairs.append(tuple(pair))
                    pair.clear()

                else:
                    pair.append(Util.parse_line(line))

        return packet_pairs

    @staticmethod
    def parse_line(line: str) -> list:
        return json.loads(line)

    @staticmethod
    def compare(a, b) -> int:
        if type(a) == int and type(b) == list:
            return Util.compare([a], b)

        if type(b) == int and type(a) == list:
            return Util.compare(a, [b])

        if type(a) == int and type(b) == int:
            return a - b

        # both are lists
        for x, y in zip(a, b):
            res = Util.compare(x, y)

            if res != 0:
                return res

        return len(a) - len(b)


class Solver:
    @staticmethod
    def solve_a(filename: str) -> int:
        signal_pairs = Util.parse_input(filename)

        pair_parity = [Util.compare(a, b) for (a, b) in signal_pairs]
        pair_indices = [idx + 1 for idx, parity in enumerate(pair_parity) if parity < 0]

        return sum(pair_indices)

    @staticmethod
    def solve_b(filename: str) -> int:
        signal_pairs = Util.parse_input(filename)
        signals = [signal for pair in signal_pairs for signal in pair]

        divider_packets = [[[2]], [[6]]]
        signals.extend(divider_packets)

        sorted_signals = sorted(signals, key=cmp_to_key(Util.compare))

        divider_indices = [
            idx + 1 for idx, key in enumerate(sorted_signals) if key in divider_packets
        ]

        return reduce(lambda x, y: x * y, divider_indices)


class TestClass:
    def test_a(self):
        out = Solver.solve_a("input_eg.txt")
        assert out == 13

    def test_b(self):
        out = Solver.solve_b("input_eg.txt")
        assert out == 140


if __name__ == "__main__":
    a = Solver.solve_a("input.txt")
    b = Solver.solve_b("input.txt")

    print(f"{a=}")
    print(f"{b=}")
