from . import esat
from .esat import esat

def emis_atm(Tair, rh, pres):
	"""Atmospheric emissivity

	Calculates the atmospheric emissivity, a necessary input to the
	calculation of globe temperature.

	:param Tair: Air temperature in Kelvin (K)
	:type Tair: float
	:param rh: Relative humidity as a proportion between 0 and 1
	:type rh: float
	:param pres: Barometric pressure in millibars (equivalent to hPa)
	:type pres: float
	:returns: the atmospheric emissivity
	:rtype: float
	:examples: emis_atm(290, 0.65, 1013)
	"""

	eee = rh * esat(Tair, 0, pres)
	return 0.575 * (eee ** 0.143)
