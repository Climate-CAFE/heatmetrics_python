import math

def humidex(t, td):
	"""Humidex

	Calculates the humidex in degrees Celsius from ambient temperature
	and dew-point temperature. If only temperature and relative humidity are known,
	then first use the function td() to calculate dew-point temperature. Relative
	humidity can be calculated from temperature, specific humidity, and barometric
	pressure using the rh() function. See equation 3 from Smoyer-Tomic and Rainham
	(2001) [https://doi.org/10.1289/ehp.011091241] and references therein.

	:param t: Ambient temperature (deg. C)
	:type t: float
	:param td: Dew-point temperature (deg. C)
	:type td: float
	:returns: the humidex in degrees Celsius.
	:rtype: float
	:examples: humidex(30, 26)
	"""

	hx = (t + (5/9) * ((6.1094 * math.exp((17.625 * td) / (243.04 + td))) - 10))
	return hx
