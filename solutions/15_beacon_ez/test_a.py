from tqdm import tqdm, trange
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
    _radius: int | None = None

    @property
    def radius(self):
        if self._radius is None:
            self._radius = Util.taxi_dist(
                self.x, self.y, self.closest_beacon.x, self.closest_beacon.y
            )

        return self._radius


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

    @staticmethod
    def point_in_range(point: Beacon, sensor: Sensor) -> bool:
        radius = sensor.radius
        distance = Util.taxi_dist(sensor.x, sensor.y, point.x, point.y)

        return distance <= radius

    @staticmethod
    def get_circumference(sensor: Sensor, limits: tuple) -> list:
        lower, upper = limits
        points = []

        radius = Util.taxi_dist(
            sensor.x, sensor.y, sensor.closest_beacon.x, sensor.closest_beacon.y
        )

        # We need all points at radius+1, the target point will be one of these
        radius = radius + 1

        for x_offset in range(0, radius + 1):
            y_offset = radius - x_offset
            circumference_points = set(
                [
                    (sensor.x - x_offset, sensor.y - y_offset),
                    (sensor.x + x_offset, sensor.y - y_offset),
                    (sensor.x - x_offset, sensor.y + y_offset),
                    (sensor.x + x_offset, sensor.y + y_offset),
                ]
            )

            valid_points = [
                p
                for p in circumference_points
                if (p[0] >= lower and p[0] <= upper)
                and (p[1] >= lower and p[1] <= upper)
            ]

            points.extend(valid_points)

        return points


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
    def solve_b_v1(filename: str, limits: tuple) -> int:
        """
        This naive version would take over 12_000_000 seconds to finish
        the search space is just too large. Abandoned this approach
        """
        sensors = Util.parse_input(filename)
        # sensors = sensors[0:2]
        print(sensors)
        lower, upper = limits

        for y in trange(lower, upper + 1):
            safe_zones = set([])
            for sensor in tqdm(sensors, total=len(sensors)):
                dist_line = abs(sensor.y - y)
                dist_beacon = Util.taxi_dist(
                    sensor.x, sensor.y, sensor.closest_beacon.x, sensor.closest_beacon.y
                )

                if dist_line > dist_beacon:
                    continue

                # Since the beacon isn't the closest spot on the line,
                # Some points on the line cannot have another beacon
                remaining_dist = dist_beacon - dist_line

                safe_zone = [
                    x
                    # for x in range(lower, upper + 1)
                    # if x >= sensor.x - remaining_dist and x <= sensor.x + remaining_dist
                    for x in range(
                        sensor.x - remaining_dist, sensor.x + remaining_dist + 1
                    )
                    if x >= lower and x <= upper
                ]
                # safe_zone = [
                #     x
                #     for x in range(lower, upper + 1)
                #     if x < sensor.x - remaining_dist or x > sensor.x + remaining_dist
                # ]

                safe_zones = safe_zones.union(safe_zone)
                # safe_zones.extend(safe_zone)
                # safe_zones.append(safe_zone)

            # print(f"{y=} {set(safe_zones)=}")
            # blind_zones = [x for x in range(lower, upper + 1) if x not in safe_zones]
            blind_zones = safe_zones  # set(safe_zones)
            # blind_zones = set(safe_zones[0])
            # for zone in safe_zones[1:]:
            #     blind_zones = blind_zones & set(zone)
            # print(f"{y=} {blind_zones=}")  # {safe_zones=}")

            if len(blind_zones) == (upper - lower):
                print(f"{blind_zones=}")
                x = [x for x in range(lower, upper + 1) if x not in blind_zones][0]
                coord = x * 4_000_000 + y
                return coord

    @staticmethod
    def solve_b_v2(filename: str, limits: tuple) -> int:
        """
        Since there's only one point, it must lie just outside the safe_zone. So the search space
        can be limited by only considering points just beyond the radius of the sensor.
        This took 31:14 minutes to complete (for my solution, it only searched the first 8 beacons)
        The following optimisations helped
        - early exit if possible when comparing a candidate point against the other beacons (this was a big one)
        - only return points in the limits from get_circumference
        - cache the radius of each beacon
        """
        sensors = Util.parse_input(filename)
        lower, upper = limits

        # Find all points in the circumference of each beacon
        for idx, sensor in enumerate(sensors):
            candidate_points = Util.get_circumference(sensor, limits)

            for (x, y) in tqdm(
                candidate_points,
                total=len(candidate_points),
                desc=f"Sensor {idx+1}/{len(sensors)}",
            ):
                if x < lower or x > upper:
                    continue
                if y < lower or y > upper:
                    continue

                for s in sensors:
                    if Util.point_in_range(Beacon(x, y), s):
                        break
                else:
                    return x * 4_000_000 + y


class TestClass:
    def test_a(self):
        out = Solver.solve_a("input_eg.txt", 10)
        assert out == 26

    def test_b(self):
        out = Solver.solve_b_v2("input_eg.txt", (0, 20))
        assert out == 56000011


if __name__ == "__main__":
    a = Solver.solve_a("input.txt", 2_000_000)
    b = Solver.solve_b_v2("input.txt", (0, 4_000_000))

    print(f"{a=}")
    print(f"{b=}")
