# core
from typing import List

def _FDTDWaveform2D(
	u_0: List[List[float, ...]],
	u_1: List[List[float, ...]],
	B: List[List[int, ...]],
	c_0: float,
	c_1: float,
	d: float,
	T: int,
	x_range: tuple[int, int],
	y_range: tuple[int, int],
	w: tuple[float, float],
) -> List[float, ...]: ...
def _raisedCosine1D(size: int, mu: int, sigma: float) -> List[float, ...]: ...
def _raisedCosine2D(size_X: int, size_Y: int, mu_x: int, mu_y: int, sigma: float) -> List[[float, ...]]: ...
