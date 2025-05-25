def net(t, RH, ws):
	"""Calculate net effective temperature (NET)

	To calculate the net effective temperature from ambient temperature,
	relative humidity, and wind speed. See section 3 of Li and Chan (2000)
	[https://doi.org/10.1017/S1350482700001602] and references therein.

	:param t: Ambient temperature (deg. C)
	:type t: float
	:param RH: Relative humidity (\%)
	:type RH: float
	:param ws: Wind speed (m/s)
	:type ws: float
	:returns: the net effective temperature in degrees Celsius.
	:rtype: float
	:examples: net(30, 75, 2)
	"""

	net = 37 - ((37 - t) / (0.68 - (0.0014 * RH) + (1 / (1.76 + 1.4 * ws ** 0.75)))) - (0.29 * t * (1 - 0.01 * RH))
	return net
