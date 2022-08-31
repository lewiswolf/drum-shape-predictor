# core
from typing import Annotated

Point = Annotated[list[float], len(2)]

def _centroid(V: list[Point], a: float) -> Point: ...
def _convexNormalisation(V: list[Point]) -> list[Point]: ...
def _generateConvexPolygon(N: int) -> list[Point]: ...
def _isColinear(V: list[Point]) -> bool: ...
def _isConvex(V: Annotated[list[Point], len(3)]) -> bool: ...
def _largestVector(V: list[Point]) -> tuple[float, tuple[int, int]]: ...
def _polygonArea(V: list[Point]) -> float: ...
