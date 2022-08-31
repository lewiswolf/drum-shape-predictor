def besselJ(n: float, m: float) -> float: ...
def besselJZero(n: float, m: int) -> float: ...
def _FDTDWaveform2D(
	u_0: list[list[float]],
	u_1: list[list[float]],
	B: list[list[int]],
	c_0: float,
	c_1: float,
	c_2: float,
	T: int,
	w: tuple[int, int],
) -> list[float]: ...
def _raisedCosine1D(size: int, mu: int, sigma: float) -> list[float]: ...
def _raisedCosine2D(size_X: int, size_Y: int, mu_x: int, mu_y: int, sigma: float) -> list[list[float]]: ...
