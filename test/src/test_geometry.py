# core
from unittest import TestCase

# dependencies
import cv2					# image processing
import numpy as np 			# maths

# src
from kac_drumset.externals._geometry import (
	_generateConvexPolygon,
	_generateIrregularStar,
	_generatePolygon,
	_isConvex,
	_normaliseConvexPolygon,
)
from kac_drumset.geometry import (
	# methods
	isColinear,
	largestVector,
	lineIntersection,
	# classes
	ConvexPolygon,
	IrregularStar,
	TSPolygon,
	UnitRectangle,
	# UnitTriangle,
	# types
	Circle,
	Polygon,
)


class GeometryTests(TestCase):
	'''
	Tests used in conjunction with `/geometry`.
	'''

	def test_circle(self) -> None:
		'''
		Test properties of the type Circle.
		'''

		# This test asserts that the center of the boolean mask is always true.
		for r in [0.1, 0.25, 0.5, 1.]:
			M = Circle(r).draw(101)
			self.assertEqual(M[50, 50], 1)
			self.assertEqual(M[0, 0], 0)
			self.assertEqual(M[0, 100], 0)
			self.assertEqual(M[100, 0], 0)
			self.assertEqual(M[100, 100], 0)

	def test_convex_polygon(self) -> None:
		'''
		Test properties of the type Polygon.
		'''

		# Two squares ordered clockwise and counter-clockwise respectively.
		squares = [
			Polygon([[0., 0.], [1., 0.], [1., 1.], [0., 1.]]),
			Polygon([[0., 0.], [0., 1.], [1., 1.], [1., 0.]]),
		]
		# The first two quads have opposite vertex order.
		# The second two quads have their x and y coordinates swapped.
		quads = [
			Polygon([[0, 0], [1.1, 0], [1, 1], [0, 1]]),
			Polygon([[0, 0], [0, 1], [1, 1], [1.1, 0]]),
			Polygon([[0, 0], [0, 1.1], [1, 1], [1, 0]]),
			Polygon([[0, 0], [1, 0], [1, 1], [0, 1.1]]),
		]

		# This test asserts that _isPointInsidePolygon works as expected
		for quad in quads:
			for p in quad.vertices:
				self.assertTrue(quad.isPointInside(p))
			for n in range(quad.N):
				a = quad.vertices[n]
				b = quad.vertices[(n + 1) % quad.N]
				self.assertTrue(quad.isPointInside(((a[0] + b[0]) / 2., (a[1] + b[1]) / 2.)))
		for square in squares:
			for p in square.vertices:
				self.assertTrue(square.isPointInside(p))
			for n in range(square.N):
				a = square.vertices[n]
				b = square.vertices[(n + 1) % square.N]
				self.assertTrue(square.isPointInside(((a[0] + b[0]) / 2., (a[1] + b[1]) / 2.)))
			self.assertTrue(square.isPointInside((0.999, 0.5)))
			self.assertFalse(square.isPointInside((1.001, 0.5)))
			self.assertTrue(square.isPointInside((0.5, 0.999)))
			self.assertFalse(square.isPointInside((0.5, 1.001)))
			self.assertTrue(square.isPointInside((0.001, 0.5)))
			self.assertFalse(square.isPointInside((-0.001, 0.5)))
			self.assertTrue(square.isPointInside((0.5, 0.001)))
			self.assertFalse(square.isPointInside((0.5, -0.001)))

			# This test asserts that a square has the correct number of vertices.
			self.assertEqual(len(square.vertices), square.N)

			# This test asserts that _isConvex works for any closed arrangement of vertices.
			self.assertTrue(square.convex)

			# This test asserts that _normaliseConvexPolygon produces the correct output.
			self.assertFalse(False in np.equal(
				np.array(_normaliseConvexPolygon(square.vertices)),
				np.array([[0., 0.5], [0.5, 1.], [1., 0.5], [0.5, 0.]]),
			))

		# This test asserts that _isSimple works as expected.
		self.assertFalse(Polygon([[0., 0.], [1., 1.], [1., 0.], [0., 1.]]).isSimple())
		for square in squares:
			self.assertTrue(square.isSimple())

		# This test asserts that after _normaliseConvexPolygon, the two squares produce the same output.
		self.assertFalse(False in np.equal(
			_normaliseConvexPolygon(squares[0].vertices),
			_normaliseConvexPolygon(squares[1].vertices)),
		)
		# This test asserts that after _normaliseConvexPolygon, the quads produce the same output.
		for quad in quads:
			quad.vertices = np.array(_normaliseConvexPolygon(quad.vertices))
		self.assertFalse(False in np.equal(quads[0].vertices, quads[1].vertices))
		# np.allclose is used, as opposed to np.equal, to account for floating point errors.
		self.assertTrue(np.allclose(quads[0].vertices, quads[2].vertices))
		self.assertTrue(np.allclose(quads[0].vertices, quads[3].vertices))

	def test_lines(self) -> None:
		'''
		Test properties of lines and curves.
		'''

		# This test asserts that lineIntersection() correctly reports none.
		does_it_cross, cross_point = lineIntersection(
			np.array([[0., 0.], [1., 0.]]),
			np.array([[0., 1.], [1., 1.]]),
		)
		self.assertEqual(does_it_cross, 'none')
		self.assertTrue(cross_point[0] == 0. and cross_point[1] == 0.)

		# This test asserts that lineIntersection() correctly reports intersection.
		does_it_cross, cross_point = lineIntersection(
			np.array([[0., 0.], [1., 0.]]),
			np.array([[0.5, -0.5], [0.5, 0.5]]),
		)
		self.assertTrue(cross_point[0] == 0.5 and cross_point[1] == 0.)

		# This test asserts that lineIntersection() correctly reports vertex.
		does_it_cross, cross_point = lineIntersection(
			np.array([[0., 0.], [1., 0.]]),
			np.array([[1., 0.], [1., 1.]]),
		)
		self.assertEqual(does_it_cross, 'vertex')
		self.assertTrue(cross_point[0] == 1. and cross_point[1] == 0.)
		does_it_cross, cross_point = lineIntersection(
			np.array([[0., 0.], [1., 1.]]),
			np.array([[1., 0.], [1., 1.]]),
		)
		self.assertEqual(does_it_cross, 'vertex')
		self.assertTrue(cross_point[0] == 1. and cross_point[1] == 1.)
		does_it_cross, cross_point = lineIntersection(
			np.array([[0., 0.], [1., 0.]]),
			np.array([[0., 0.], [1., 1.]]),
		)
		self.assertEqual(does_it_cross, 'vertex')
		self.assertTrue(cross_point[0] == 0. and cross_point[1] == 0.)
		does_it_cross, cross_point = lineIntersection(
			np.array([[0., 1.], [1., 1.]]),
			np.array([[0., 0.], [0., 1.]]),
		)
		self.assertEqual(does_it_cross, 'vertex')
		self.assertTrue(cross_point[0] == 0. and cross_point[1] == 1.)

		# This test asserts that lineIntersection() correctly reports adjacent.
		does_it_cross, cross_point = lineIntersection(
			np.array([[0., 0.], [1., 0.]]),
			np.array([[0.5, 0.], [0.5, 1.]]),
		)
		self.assertEqual(does_it_cross, 'adjacent')
		self.assertTrue(cross_point[0] == 0.5 and cross_point[1] == 0.)
		does_it_cross, cross_point = lineIntersection(
			np.array([[0.5, 0.], [0.5, 1.]]),
			np.array([[0., 0.], [1., 0.]]),
		)
		self.assertEqual(does_it_cross, 'adjacent')
		self.assertTrue(cross_point[0] == 0.5 and cross_point[1] == 0.)

		# This test asserts that lineIntersection() correctly reports colinear.
		does_it_cross, cross_point = lineIntersection(
			# B inside
			np.array([[0., 0.], [1., 0.]]),
			np.array([[0.25, 0.], [0.75, 0.]]),
		)
		self.assertEqual(does_it_cross, 'colinear')
		self.assertTrue(cross_point[0] == 0.5 and cross_point[1] == 0.)
		does_it_cross, cross_point = lineIntersection(
			# B left
			np.array([[0., 0.], [1., 0.]]),
			np.array([[-0.5, 0.], [0.5, 0.]]),
		)
		self.assertEqual(does_it_cross, 'colinear')
		self.assertTrue(cross_point[0] == 0.25 and cross_point[1] == 0.)
		does_it_cross, cross_point = lineIntersection(
			# B right
			np.array([[0., 0.], [1., 0.]]),
			np.array([[-0.5, 0.], [1.5, 0.]]),
		)
		self.assertEqual(does_it_cross, 'colinear')
		self.assertTrue(cross_point[0] == 0.5 and cross_point[1] == 0.)
		does_it_cross, cross_point = lineIntersection(
			# A inside
			np.array([[0.25, 0.], [0.75, 0.]]),
			np.array([[0., 0.], [1., 0.]]),
		)
		self.assertEqual(does_it_cross, 'colinear')
		self.assertTrue(cross_point[0] == 0.5 and cross_point[1] == 0.)
		does_it_cross, cross_point = lineIntersection(
			# A left
			np.array([[-0.5, 0.], [0.5, 0.]]),
			np.array([[0., 0.], [1., 0.]]),
		)
		self.assertEqual(does_it_cross, 'colinear')
		self.assertTrue(cross_point[0] == 0.25 and cross_point[1] == 0.)
		does_it_cross, cross_point = lineIntersection(
			# A right
			np.array([[-0.5, 0.], [1.5, 0.]]),
			np.array([[0., 0.], [1., 0.]]),
		)
		self.assertEqual(does_it_cross, 'colinear')
		self.assertTrue(cross_point[0] == 0.5 and cross_point[1] == 0.)

	def test_random_polygon(self) -> None:
		'''
		Stress test multiple properties of random polygons.
		'''

		for i in range(10000):
			# This test asserts that _generateConvexPolygon always produces a unique output.
			self.assertFalse(np.all(np.equal(_generateConvexPolygon(3), _generateConvexPolygon(3))))
			self.assertFalse(np.all(np.equal(_generateIrregularStar(3), _generateIrregularStar(3))))
			self.assertFalse(np.all(np.equal(_generatePolygon(3), _generatePolygon(3))))

			for P in [
				ConvexPolygon,
				IrregularStar,
				TSPolygon,
			]:
				polygon = P(max_vertices=20)
				LV = largestVector(polygon.vertices)

				# This test asserts that a polygon has the correct number of vertices.
				self.assertEqual(len(polygon.vertices), polygon.N)

				# This test asserts that a polygon has is simple.
				self.assertTrue(polygon.isSimple())

				# This test asserts that the vertices are strictly bounded between 0.0 and 1.0.
				self.assertEqual(polygon.vertices.min(), 0.)
				self.assertEqual(polygon.vertices.max(), 1.)

				# This test asserts that the largest vector is of magnitude 1.0.
				self.assertEqual(LV[0], 1.)

				# This test asserts that the area(), used for calculating the area of a polygon is accurate to at least 6 decimal
				# places. This comparison is bounded due to the area() being 64-bit, whilst the comparison function,
				# cv2.contourArea(), is 32-bit.
				self.assertAlmostEqual(
					polygon.area(),
					cv2.contourArea(polygon.vertices.astype('float32')),
					places=7,
				)

				# This test asserts that no 3 adjacent vertices are colinear.
				for n in range(polygon.N):
					self.assertFalse(isColinear(np.array([
						polygon.vertices[n - 1 if n > 0 else polygon.N - 1],
						polygon.vertices[n],
						polygon.vertices[(n + 1) % polygon.N],
					])))

			if polygon.convex:
				# This test asserts that all supposedly convex polygons are in fact convex. As a result, if this test passes, we
				# can assume that the _generateConvexPolygon() function works as intended.
				self.assertTrue(_isConvex(polygon.vertices))

				# This test asserts that the largest vector lies across the x-axis.
				self.assertTrue(polygon.vertices[LV[1][0]][0] == 0.)
				self.assertTrue(polygon.vertices[LV[1][1]][0] == 1.)

				# This test asserts that the calculated centroid lies within the polygon. For concave shapes, this test may fail.
				centroid = polygon.centroid()
				polygon.isPointInside(centroid)
				self.assertEqual(polygon.draw(100)[
					round(centroid[0] * 99),
					round(centroid[1] * 99),
				], 1)

				# This test asserts that _normaliseConvexPolygon does not continuously alter the polygon.
				# np.allclose is used, as opposed to np.equal, to account for floating point errors.
				self.assertTrue(np.allclose(polygon.vertices, np.array(_normaliseConvexPolygon(polygon.vertices))))

	def test_unit_polygon(self) -> None:
		'''
		Test used in conjunction with ./unit_polygons.py.
		'''

		# Test the vertices, centroid and area of the UnitRectangle for varying epsilons.
		for [epsilon, vertices] in [
			(1., [[0.5, 0.5], [0.5, -0.5], [-0.5, -0.5], [-0.5, 0.5]]),
			(0.5, [[0.25, 1.], [0.25, -1.], [-0.25, -1.], [-0.25, 1.]]),
			(1.25, [[0.625, 0.4], [0.625, -0.4], [-0.625, -0.4], [-0.625, 0.4]]),
		]:
			R = UnitRectangle(epsilon)
			P = Polygon(vertices)
			self.assertTrue(np.all(np.equal(R.vertices, P.vertices)))
			self.assertEqual(R.area(), P.area())
			self.assertEqual(R.centroid(), (0., 0.))

		# Test the vertices and area of the UnitTriangle for varying r, theta.
		# for [r, theta] in [
		# 	(0.5, np.pi / 2.),
		# 	(1., 1.),
		# 	(1., 2.),
		# 	(1., 3.),
		# 	(1., 4.),
		# 	(1., 5.),
		# 	(1., 6.),
		# ]:
		# 	T = UnitTriangle(1., np.pi / 3)
		# 	P = Polygon(T.vertices)
		# 	self.assertAlmostEqual(T.area(), P.area())
		# 	self.assertEqual(T.vertices[:, 0].min() + T.vertices[:, 0].max(), 0.)
		# 	self.assertEqual(T.vertices[:, 1].min() + T.vertices[:, 1].max(), 0.)

		# # This tests asserts the symmetry of the method used to generate UnitTriangle
		# norm_tri = normaliseConvexPolygon(UnitTriangle(1., 1.))
		# self.assertTrue(np.all(np.allclose(normaliseConvexPolygon(UnitTriangle(1., np.pi - 1.)), norm_tri)))
		# self.assertTrue(np.all(np.allclose(normaliseConvexPolygon(UnitTriangle(1., np.pi + 1.)), norm_tri)))
		# self.assertTrue(np.all(np.allclose(normaliseConvexPolygon(UnitTriangle(1., -1.)), norm_tri)))

		# # This test asserts that the equilateral triangle is properly constructed.
		# T = UnitTriangle(1., np.pi / 2)
		# for n in range(3):
		# 	a = T.vertices[n]
		# 	b = T.vertices[(n + 1) % 3]
		# 	self.assertEqual(
		# 		((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2) ** 0.5,
		# 		(4 / (3 ** 0.5)) ** 0.5,
		# 	)
