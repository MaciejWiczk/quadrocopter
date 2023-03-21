import math
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Point:
    """
    Class to represent Point
    """

    x: int
    y: int


@dataclass
class Radar:
    """
    Class to represent Radar and it's center
    """

    center: Point
    radius: int

    def covers_point(self, point: Point) -> bool:
        """
        Checks if point is within radar coverage, and return True if so.
        """
        return (point.x - self.center.x) ** 2 + (point.y - self.center.y) ** 2 <= self.radius**2


def _radars_overlap(first_radar: Radar, second_radar: Radar) -> bool:
    """
    Checks if one radar range is connected with other radar range.
    """
    dist: float = math.sqrt(
        (first_radar.center.x - second_radar.center.x) ** 2 + (first_radar.center.y - second_radar.center.y) ** 2
    )
    if (
        (dist <= first_radar.radius - second_radar.radius)
        or (dist <= second_radar.radius - first_radar.radius)
        or (dist <= first_radar.radius + second_radar.radius)
    ):
        return True
    else:
        return False


def _build_graph(radars: list[Radar]) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = defaultdict(list)
    for i, radar in enumerate(radars):
        for j, _radar in enumerate(radars):
            if _radars_overlap(first_radar=radar, second_radar=_radar):
                graph[i].append(j)
    return graph


def check_quadrocopter_route(start: Point, finish: Point, radars: list[Radar]) -> bool:
    """
    Entrypoint for verifying possibility of quadrocopter flight from start to finish.
    """
    graph = _build_graph(radars)
    starting_radars: list[int] = _get_radars_covering_point(start, radars)
    finishing_radars: list[int] = _get_radars_covering_point(finish, radars)
    if set(starting_radars).intersection(finishing_radars):
        return True
    return any(
        _path_exists(starting_radar, finishing_radar, graph)
        for starting_radar in starting_radars
        for finishing_radar in finishing_radars
    )


def _path_exists(start: int, finish: int, graph: dict[str, list[str]], path: list[str] = []) -> bool:
    path = path + [start]
    if start == finish:
        return True
    if start not in graph.keys():
        return False
    for node in graph[start]:
        if node not in path:
            if _path_exists(node, finish, graph, path):
                return True
    return False


def _get_radars_covering_point(point: Point, radars: list[Radar]) -> list[int]:
    return [i for i, radar in enumerate(radars) if radar.covers_point(point)]
