# coding: utf-8

import numpy as np


def ellips(t, e):
	"""
	Cartesian coordinates of the ellipse point at a given parameter.

	Parameters
	----------
	t : float or numpy.ndarray
		Parameter -- angle.
	e : float
		Eccentricity.

	Returns
	-------
	[x, y] : list
		Cartesian coordinates of the ellipse point at a given parameter.
	"""
	
	x = np.cos(t)
	y = np.sqrt(1-e)*np.sin(t)

	return [x, y]


def solve_kepler_equation(t, e):
	"""
	The solution of the Kepler equation.

	Parameters
	----------
	t : float
		Time.
	e : float
		Eccentricity.

	Returns
	-------
	E : float
		Eccentric anomaly.
	"""

	if (t == 0):
		E = 0
	
	else:
		E0 = t

		while True:
			E = t + e*np.sin(E0)

			if (abs((E-E0)/E) <= 1e-10): break

			E0 = E

	return E % (2*np.pi)


def r(t, e):
	"""
	Half the distance between the attracting bodies.

	Parameters
	----------
	t : float
		Time.
	e : float
		Eccentricity.

	Returns
	-------
	f : float
		Half the distance between the attracting bodies.
	"""
		
	E = solve_kepler_equation(t, e)

	f = (1 - e*np.cos(E)) / 2

	return f


def differ2(t, zv, e):
	"""
	The system of differential equations in the Sitnikov problem.

	Parameters
	----------
	t : float
		Time.
	zv : list
		Coordinate and velocity.
	e : float
		Eccentricity.

	Returns
	-------
	[dzdt, dvdt] : list
		Velocity and acceleration.
	"""

	r_te = r(t, e)

	dvdt = -zv[0] / (zv[0]**2+r_te**2)**(3/2)
	dzdt = zv[1]

	return [dzdt, dvdt]
