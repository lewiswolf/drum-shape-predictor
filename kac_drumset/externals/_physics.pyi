def besselJ(n: float, m: float) -> float: ...
def besselJZero(n: float, m: int) -> float: ...
def _FDTDWaveform2D(
	u_0: [[float, ...], ...],
	u_1: [[float, ...], ...],
	B: [[int, ...]],
	c_0: float,
	c_1: float,
	d: float,
	T: int,
	w: tuple[int, int],
) -> [float, ...]: ...
def _raisedCosine1D(size: int, mu: int, sigma: float) -> [float, ...]: ...
def _raisedCosine2D(size_X: int, size_Y: int, mu_x: int, mu_y: int, sigma: float) -> [[float, ...], ...]: ...
