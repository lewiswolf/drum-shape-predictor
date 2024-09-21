<!-- ![Kac-Drumming](https://user-images.githubusercontent.com/55607290/169860844-7f3f3d6d-4366-4410-8a30-5ee9472c2864.png) -->

# kac_drumset

![python version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)
<a href="https://doi.org/10.5281/zenodo.7274474">
![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.7274474-blue)
</a>

Python based analysis tools and dataset generator for arbitrarily shaped drums.

# Install

```bash
pip install "git+https://github.com/lewiswolf/kac_drumset.git"
```

### Dependencies

-	[cmake](https://formulae.brew.sh/formula/cmake)
-   [libsndfile](https://github.com/libsndfile/libsndfile)

# Core Library

<details>
<summary>Geometry</summary>

### Import

```python
from kac_drumset.geometry import (
	# Methods
	isColinear,
	largestVector,
	lineIntersection,
	weylCondition,
	# Classes
	Circle,
	ConvexPolygon,
	IrregularStar,
	TravellingSalesmanPolygon,
	UnitRectangle,
	# Types
	Ellipse,
	Polygon,
	Shape,
	ShapeSettings,
)
```

### Methods

```python
def isColinear(vertices: npt.NDArray[np.float64]) -> bool:
	'''
	Determines whether or not a given set of three vertices are colinear.
	'''

def largestVector(vertices: npt.NDArray[np.float64]) -> tuple[float, tuple[int, int]]:
	'''
	This function tests each pair of vertices in a given set of points to find the largest vector, and returns the length
	of the vector and its indices.
	'''

def lineIntersection(A: npt.NDArray[np.float64], B: npt.NDArray[np.float64]) -> tuple[
	Literal['adjacent', 'colinear', 'intersect', 'none', 'vertex'],
	npt.NDArray[np.float64],
]:
	'''
	This function determines whether a line has an intersection, and returns it's type as well
	as the point of intersection (if one exists).
	input
		A, B - Line segments to compare.
	output
		type -
			'none'		No intersection.
			'intersect' The general case where lines intersect one another.
			'vertex'	This is the special case when two lines share a vertex.
			'branch'	This is the special case when a vertex lies within another line. For
						example, B creates an intersection at point B.a when B.a lies on the
						open interval (A.a, A.b).
			'colinear'	This is the special case when the two lines overlap.
		point -
			'none'		Empty point.
			'intersect' The point of intersection ∈ (A.a, A.b) & (B.a, B.b).
			'vertex'	The shared vertex.
			'branch'	The branching vertex.
			'colinear'	The midpoint between all 4 vertices.
	'''

def weylCondition(S_1: Shape, S_2: Shape) -> bool:
	'''
	Using Weyl's asymptotic law, determine whether two polygons may be isospectral.
	https://en.wikipedia.org/wiki/Weyl_law
	'''
```

### Classes

```python

class Circle(Ellipse):
	'''
	A base class for a circle, instantiated with a radius.
	'''

	class Settings(ShapeSettings, total=False):
		''' Settings to be used when generating. '''
		r: float			# radius (randomly generated when r = 0)

	def __init__(self, r: float = 0., centroid: tuple[float, float] = (0., 0.)) -> None:

class ConvexPolygon(Polygon):
	'''
	Generate convex shapes according to Pavel Valtr's 1995 algorithm.
	'''

	class Settings(ShapeSettings, total=False):
		''' Settings to be used when generating. '''
		N: int				# number of vertices (randomly generated when N < 3)
		max_vertices: int	# maximum number of vertices when generating

	def __init__(self, N: int = 0, max_vertices: int = 10) -> None:

class IrregularStar(Polygon):
	'''
	This is a fast method for generating concave polygons, particularly with a large number of vertices. This approach
	generates polygons by ordering a series of random points around a centre point. As a result, not all possible simple
	polygons are generated this way.
	'''

	class Settings(ShapeSettings, total=False):
		''' Settings to be used when generating. '''
		N: int				# number of vertices (randomly generated when N < 3)
		max_vertices: int	# maximum number of vertices when generating

	def __init__(self, N: int = 0, max_vertices: int = 10) -> None:

class TravellingSalesmanPolygon(Polygon):
	'''
	This algorithm is based on a method of eliminating self-intersections in a polygon by using the Lin and Kerningham
	'2-opt' moves. Such a move eliminates an intersection between two edges by reversing the order of the vertices between
	the edges. Intersecting edges are detected using a simple sweep through the vertices and then one intersection is
	chosen at random to eliminate after each sweep.
	van Leeuwen, J., & Schoone, A. A. (1982). Untangling a traveling salesman tour in the plane.
	'''

	class Settings(ShapeSettings, total=False):
		''' Settings to be used when generating. '''
		N: int				# number of vertices (randomly generated when N < 3)
		max_vertices: int	# maximum number of vertices when generating

	def __init__(self, N: int = 0, max_vertices: int = 10) -> None:

class UnitRectangle(Polygon):
	'''
	Define a rectangle with unit area and an aspect ration epsilon.
	'''

	class Settings(ShapeSettings, total=False):
		''' Settings to be used when generating. '''
		epsilon: float		# aspect ratio (randomly generated when epsilon = 0)

	def __init__(self, epsilon: float = 0.) -> None:
```

### Types

```python
class Ellipse(Shape):
	'''
	A base class for an ellipse, instantiated with two foci.
	'''

	major: float			# length across the x axis
	minor: float			# length across the y axis

	class Settings(ShapeSettings, total=False):
		''' Settings to be used when generating. '''
		major: float		# length across the x axis
		minor: float		# length across the y axis (randomly generated when minor = 0.)

	def __init__(self, major: float = 1., minor: float = 0., centroid: tuple[float, float] = (0., 0.)) -> None:

	@property
	def area(self) -> float:
		'''
		Getters and setters for area. Setting area scales the ellipse.
		'''

	@property
	def centroid(self) -> tuple[float, float]:
		'''
		Getters and setters for centroid. Setting centroid translates the ellipse about the plane.
		'''

	def draw(self, grid_size: int) -> npt.NDArray[np.int8]:
		'''
		This function creates a boolean mask of a manifold on a grid with dimensions R^(grid_size). The input shape is always
		normalised to the domain R^G before being drawn.
		'''

	def eccentricity(self) -> float:
		'''
		The ratio between the focal distance and the major axis.
		'''

	def foci(self) -> tuple[tuple[float, float], tuple[float, float]]:
		'''
		The foci are the two points at which the sum of the distances between any point on the surface of the ellipse is a
		constant.
		'''

	def focalDistance(self) -> float:
		'''
		The distance between a focus and the centroid.
		'''

	def isPointInside(self, p: tuple[float, float]) -> bool:
		'''
		Determines if a given point p ∈ P, including boundaries.
		'''

class Polygon(Shape):
	'''
	A base class for a polygon, instantiated with an array of vertices.
	'''

	class Settings(ShapeSettings, total=False):
		''' Settings to be used when generating. '''
		vertices: list[list[float]] | npt.NDArray[np.float64]

	def __init__(self, vertices: list[list[float]] | npt.NDArray[np.float64]) -> None:

	@property
	def area(self) -> float:
		'''
		An implementation of the polygon area algorithm derived using Green's Theorem.
		'''

	@property
	def centroid(self) -> tuple[float, float]:
		'''
		Getters and setters for centroid. Setting centroid translates the polygon about the plane.
		'''

	@property
	def convex(self) -> bool:
		'''
		A cached variable representing the convexity of the polygon.
		'''

	@property
	def vertices(self) -> npt.NDArray[np.float64]:
		'''
		The vertices of the polygon, here exposed as a mutable property.
		'''

	@property
	def N(self) -> int:
		'''
		A cached variable representing the number of vertices.
		'''

	def draw(self, grid_size: int) -> npt.NDArray[np.int8]:
		'''
		This function creates a boolean mask of a manifold on a grid with dimensions R^(grid_size). The input shape is always
		normalised to the domain R^G before being drawn.
		'''

	def isPointInside(self, p: tuple[float, float]) -> bool:
		'''
		Determines if a given point p ∈ P, including boundaries.
		'''

	def isSimple(self) -> bool:
		'''
		Determine if a polygon is simple by checking for intersections.
		'''

class Shape(ABC):
	'''
	An abstract base class for a two dimensional manifold in Euclidean geometry.
	'''

	def __init__(self) -> None:
		pass

	@abstractmethod
	class Settings(ShapeSettings, total=False):
		'''
		Settings to be used when generating.
		'''

	@abstractmethod
	def __getLabels__(self) -> dict[str, list[float | int]]:
		'''
		This method should be used to return the metadata about the current shape.
		'''

	@property
	@abstractmethod
	def area(self) -> float:
		'''
		Calculate the area of a 2D manifold. This property should be used to scale the shape whenever it is set.
		'''

	@property
	@abstractmethod
	def centroid(self) -> tuple[float, float]:
		'''
		This algorithm is used to calculate the geometric centroid of a 2D manifold. This property should be used move the
		shape about the plane whenever it is set.
		'''

	@abstractmethod
	def draw(self, grid_size: int) -> npt.NDArray[np.int8]:
		'''
		This function creates a boolean mask of a manifold on a grid with dimensions R^(grid_size). The input shape is always
		normalised to the domain R^G before being drawn.
		'''

	@abstractmethod
	def isPointInside(self, p: tuple[float, float]) -> bool:
		'''
		Determines if a given point p ∈ P, including boundaries.
		'''

class ShapeSettings(TypedDict, total=False):
	''' Placeholder for custom ShapeSettings. '''
```
</details>

<details>
<summary>Physics</summary>

### Import

```python
from kac_drumset.physics import (
	# methods
	besselJ,
	besselJZero,
	circularAmplitudes,
	circularChladniPattern,
	circularSeries,
	equilateralTriangleAmplitudes,
	equilateralTriangleSeries,
	FDTDWaveform2D,
	raisedCosine,
	raisedTriangle,
	rectangularAmplitudes,
	rectangularChladniPattern,
	rectangularSeries,
	WaveEquationWaveform2D,
	# classes
	FDTD_2D
)
```

### Methods

```python
def besselJ(n: float, m: float) -> float:
	'''
	Calculate the bessel function of the first kind. This method is a clone of boost::math::cyl_bessel_j.
	'''

def besselJZero(n: float, m: int) -> float:
	'''
	Calculate the mth zero crossing of the nth bessel function of the first kind. This method is a clone of
	boost::math::cyl_bessel_j_zero.
	'''

def circularAmplitudes(r: float, theta: float, S: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
	'''
	Calculate the amplitudes of the circular eigenmodes relative to a polar strike location.
	input:
		( r, θ ) = polar strike location
		S = { z_nm | s ∈ ℝ, J_n(z_nm) = 0, 0 <= n < N, 0 < m <= M }
	output:
		A = {
			J_n(z_nm * r) * (2 ** 0.5) * sin(nθπ/4)
			| a ∈ ℝ, J_n(z_nm) = 0, 0 <= n < N, 0 < m <= M
		}
	'''

def circularChladniPattern(n: float, m: float, H: int, tolerance: float = 0.1) -> npt.NDArray[np.float64]:
	'''
	Produce the 2D chladni pattern for a circular plate.
	http://paulbourke.net/geometry/chladni/
	input:
		n = nth modal index
		m = mth modal index
		H = length of the X and Y axis
		tolerance = the standard deviation between the calculation and the final pattern
	output:
		M = {
			J_n(z_nm * r) * (cos(nθ) + sin(nθ)) ≈ 0
		}
	'''

def circularSeries(N: int, M: int) -> npt.NDArray[np.float64]:
	'''
	Calculate the eigenmodes of a circle.
	input:
		N = number of modal orders
		M = number of modes per order
	output:
		S = { z_nm | s ∈ ℝ, J_n(z_nm) = 0, n < N, 0 < m <= M }
	'''

def equilateralTriangleAmplitudes(u: float, v: float, w: float, N: int, M: int) -> npt.NDArray[np.float64]:
	'''
	Calculate the amplitudes of the equilateral triangle eigenmodes relative to a
	trilinear strike location according to Lamé's formula.
	Seth (1940) Transverse Vibrations of Triangular Membranes.
	input:
		( u, v, w ) = trilinear coordinate
		N = number of modal orders
		M = number of modes per order
	output:
		A = {
			abs(sin(nuπ) sin(nvπ) sin(nwπ))
			| a ∈ ℝ, 0 < n <= N, 0 < m <= M
		}
	'''

def equilateralTriangleSeries(N: int, M: int) -> npt.NDArray[np.float64]:
	'''
	Calculate the eigenmodes of an equilateral triangle according to Lamé's formula.
	Seth (1940) Transverse Vibrations of Triangular Membranes.
	input:
		N = number of modal orders
		M = number of modes per order
	output:
		S = {
			(m ** 2 + n ** 2 + mn) ** 0.5
			| s ∈ ℝ, 0 < n <= N, 0 < m <= M
		}
	'''

def rectangularAmplitudes(p: tuple[float, float], N: int, M: int, epsilon: float) -> npt.NDArray[np.float64]:
	'''
	Calculate the amplitudes of the rectangular eigenmodes relative to a cartesian strike location.
	input:
		( x , y ) = cartesian product
		N = number of modal orders
		M = number of modes per order
		epsilon = aspect ratio of the rectangle
	output:
		A = {
			sin(mxπ / (Є ** 0.5)) sin(nyπ * (Є ** 0.5))
			| a ∈ ℝ, 0 < n <= N, 0 < m <= M
		}
	'''

def rectangularChladniPattern(n: float, m: float, X: int, Y: int, tolerance: float = 0.1) -> npt.NDArray[np.float64]:
	'''
	Produce the 2D chladni pattern for a rectangular plate.
	http://paulbourke.net/geometry/chladni/
	input:
		n = nth modal index
		m = mth modal index
		X = length of the X axis
		Y = length of the Y axis
		tolerance = the standard deviation between the calculation and the final pattern
	output:
		M = {
			cos(nπx/X) cos(mπy/Y) - cos(mπx/X) cos(nπy/Y) ≈ 0
		}
	'''

def rectangularSeries(N: int, M: int, epsilon: float) -> npt.NDArray[np.float64]:
	'''
	Calculate the eigenmodes of a rectangle.
	input:
		N = number of modal orders
		M = number of modes per order
		epsilon = aspect ratio of the rectangle
	output:
		S = {
			((m ** 2 / Є) + (Єn ** 2)) ** 0.5
			| s ∈ ℝ, 0 < n <= N, 0 < m <= M
		}
	'''

def FDTDWaveform2D(
	u_0: npt.NDArray[np.float64],
	u_1: npt.NDArray[np.float64],
	B: npt.NDArray[np.int8],
	c_0: float,
	c_1: float,
	c_2: float,
	T: int,
	w: tuple[float, float],
) -> npt.NDArray[np.float64]:
	'''
	Generates a waveform using a 2 dimensional FDTD scheme.
	input:
		u_0 = initial fdtd grid at t = 0.
		u_1 = initial fdtd grid at t = 1.
		B = boundary conditions.
		c_0 = first fdtd coefficient related to the decay term and the courant number.
		c_1 = second fdtd coefficient related to the decay term and the courant number.
		c_2 = third fdtd coefficient related to the decay term.
		T = length of simulation in samples.
		w = the coordinate at which the waveform is sampled ∈ ℝ^2, [0. 1.].
	output:
		waveform = W[n] ∈
			c_0 * (
				u_n_x+1_y + u_n_x-1_y + u_n_x_y+1 + u_n_x_y-1
			) + c_1 * u_n_x_y - c_2 * (u_n-1_x_y) ∀ u ∈ R^2
	'''

def raisedCosine(
	matrix_size: tuple[int, ...],
	mu: tuple[float] | tuple[float, float],
	sigma: float = 0.5,
) -> npt.NDArray[np.float64]:
	'''
	Creates a raised cosine distribution centred at mu. Only 1D and 2D distributions are supported.
	input:
		matrix_size = A tuple representing the size of the output matrix.
		μ = The coordinate used to represent the centre of the cosine distribution.
		σ = The radius of the distribution.
	'''

def raisedTriangle(
	matrix_size: tuple[int, ...],
	mu: tuple[float] | tuple[float, float],
	x_ab: tuple[float, float] | None = None,
	y_ab: tuple[float, float] | None = None,
) -> npt.NDArray[np.float64]:
	'''
	Calculate a one or two dimensional triangular distribution.
	input:
		size = the size of the matrix.
		μ = a cartesian point representing the maxima of the triangle.
		x_ab = minimum and maximum x value for the distribution.
		y_ab = minimum and maximum y value for the distribution.
	output:
		Λ(x, y) = Λ(x) * Λ(y)
		Λ(x) = {
			0,								x < a
			(x - a) / (μ - a),				a ≤ x ≤ μ
			1. - (x - μ) / (b - μ),			μ < x ≤ b
			0,								x > a
		}
	'''

def WaveEquationWaveform2D(
	F: npt.NDArray[np.float64],
	A: npt.NDArray[np.float64],
	d: float,
	k: float,
	T: int,
) -> npt.NDArray[np.float64]:
	'''
	Calculate a closed form solution to the 2D wave equation.
	input:
		F = frequencies (hertz)
		A = amplitudes ∈ [0, 1]
		d = decay
		k = sample length
		T = length of simulation
	output:
		waveform = W[t] ∈ A * e^dt * sin(ωt) / max(A) * NM
	'''
```

### Classes

```python
class FDTD_2D():
	'''
	Class implementation of a two dimensional FDTD equation. This method is designed to be used as an iterator:
	for u in FDTD(*args):
		print(u)
	input:
		u_0 = initial fdtd grid at t = 0.
		u_1 = initial fdtd grid at t = 1.
		B = boundary condition.
		c_0 = first fdtd coefficient related to the decay term and the courant number.
		c_1 = second fdtd coefficient related to the decay term and the courant number.
		c_2 = third fdtd coefficient related to the decay term.
		T = length of simulation.
	output:
		u[n] = c_0 * (
			u_x+1_y + u_0_x-1_y + u_0_x_y+1 + u_0_x_y-1
		) + c_1 * u_0_x_y - c_2 * (u_1_x_y)
	'''

	def __init__(
		self,
		u_0: list[list[float]],
		u_1: list[list[float]],
		B: list[list[int]],
		c_0: float,
		c_1: float,
		c_2: float,
		T: int,
	) -> None:
		''' Initialise FDTD iterator. '''
	
	def __iter__(self) -> 'FDTD_2D':
		''' Return the iterator. '''

	def __next__(self) -> npt.NDArray[np.float64]:
		''' Compute the FDTD update equation at every iteration. '''
```

</details>

<details><summary>Samplers</summary>

### Import

```python
from kac_drumset.samplers import (
	BesselModel,
	FDTDModel,
	LaméModel,
	PoissonModel,
)
```

### Classes

```python
class BesselModel(AudioSampler):
	'''
	A linear model of a circular membrane using bessel equations of the first kind.
	'''

	class Settings(SamplerSettings, total=False):
		M: int						# number of mth modes
		N: int						# number of nth modes
		amplitude: float			# maximum amplitude of the simulation ∈ [0, 1]
		decay_time: float			# how long will the simulation take to decay? (seconds)
		material_density: float		# material density of the simulated drum membrane (kg/m^2)
		tension: float				# tension at rest (N/m)

class FDTDModel(AudioSampler):
	'''
	This class creates a 2D simulation of an arbitrarily shaped drum, calculated using a FDTD scheme.
	'''

	class Settings(SamplerSettings, total=False):
		amplitude: float				# maximum amplitude of the simulation ∈ [0, 1]
		arbitrary_shape: type[Shape]	# what shape should the drum be in?
		decay_time: float				# how long will the simulation take to decay? (seconds)
		drum_size: float				# size of the drum, spanning both the horizontal and vertical axes (m)
		material_density: float			# material density of the simulated drum membrane (kg/m^2)
		shape_settings: ShapeSettings	# the class generator settings for a given drum shape
		strike_width: float				# width of the drum strike (m)
		tension: float					# tension at rest (N/m)

class LaméModel(AudioSampler):
	'''
	A linear model of an equilateral triangle membrane using Lamé equations.
	'''

	class Settings(SamplerSettings, total=False):
		M: int						# number of mth modes
		N: int						# number of nth modes
		amplitude: float			# maximum amplitude of the simulation ∈ [0, 1]
		decay_time: float			# how long will the simulation take to decay? (seconds)
		material_density: float		# material density of the simulated drum membrane (kg/m^2)
		tension: float				# tension at rest (N/m)

class PoissonModel(AudioSampler):
	'''
	A linear model of a unit area rectangle with aspect ratio Є, using poisson equations of the first kind.
	'''

	class Settings(SamplerSettings, total=False):
		M: int						# number of mth modes
		N: int						# number of nth modes
		amplitude: float			# maximum amplitude of the simulation ∈ [0, 1]
		decay_time: float			# how long will the simulation take to decay? (seconds)
		material_density: float		# material density of the simulated drum membrane (kg/m^2)
		tension: float				# tension at rest (N/m)
```
</details>

# Development

### Dependencies

-   [pipenv](https://formulae.brew.sh/formula/pipenv#default)

### Install

```bash
git clone --recursive ...
pipenv install -d
```
### Build C++ Backend

```bash
pipenv run build
```
### Example

```
pipenv run start
```
### Test

```
pipenv run test
```