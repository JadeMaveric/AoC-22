from dataclasses import dataclass
import re


@dataclass
class Beacon:
    x: int
    y: int


@dataclass
class Sensor:
    x: int
    y: int
    closest_beacon: Beacon


class Util:
    @staticmethod
    def parse_input(filename: str) -> list:
        sensors = []

        REGEX = re.compile(r"x=(-?\d+), y=(-?\d+)")

        with open(filename) as data:
            for line in data.readlines():
                try:
                    sensor, beacon = REGEX.findall(line)
                except ValueError as e:
                    print(line)
                    raise e

                b_obj = Beacon(int(beacon[0]), int(beacon[1]))
                s_obj = Sensor(int(sensor[0]), int(sensor[1]), b_obj)

                sensors.append(s_obj)

        return sensors

    @staticmethod
    def taxi_dist(x1: int, y1: int, x2: int, y2: int) -> int:
        return abs(x1 - x2) + abs(y1 - y2)


class Solver:
    @staticmethod
    def solve_a(filename: str, y: int) -> int:
        sensors = Util.parse_input(filename)
        safe_zones = []

        # Find horizontal distance from each sensor to the target line
        # Compare this distance to the closest beaon
        # If it's higher, the delta of the two distances gives positions
        # where the beacon cannot be
        for sensor in sensors:
            dist_line = abs(sensor.y - y)
            dist_beacon = Util.taxi_dist(
                sensor.x, sensor.y, sensor.closest_beacon.x, sensor.closest_beacon.y
            )

            if dist_line > dist_beacon:
                continue

            # Since the beacon isn't the closest spot on the line,
            # Some points on the line cannot have another beacon
            remaining_dist = dist_beacon - dist_line
            safe_zone = list(
                range(sensor.x - remaining_dist, sensor.x + remaining_dist)
            )

            safe_zones.extend(safe_zone)

        return len(set(safe_zones))

    @staticmethod
    def solve_b(filename: str) -> int:
        ...


class TestClass:
    def test_a(self):
        out = Solver.solve_a("input_eg.txt", 10)
        assert out == 26

    def test_b(self):
        ...
        # out = Solver.solve_b("input_eg.txt")
        # assert out == 8


if __name__ == "__main__":
    a = Solver.solve_a("input.txt", 2_000_000)
    # b = Solver.solve_b("input.txt")

    print(f"{a=}")
    # print(f"{b=}")
