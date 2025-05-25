import math

def esat(tk, phase, Pair):
    """Saturation vapor pressure

    Calculates the saturation vapor pressure (mb) over liquid water
    (phase = 0) or ice (phase = 1).

    :param tk: Air temperature in Kelvin (K)
    :type tk: float
    :param phase: Over liquid water (0) or ice (1)
    :type phase: int
    :param Pair: Barometric pressure in millibars (equivalent to hPa)
    :type Pair: float
    :returns the saturation vapor pressure in millibars (equivalent to hPa).
    :rtype: float
    :examples: esat(293, 0, 1014)
    """

    if phase == 0:
        y = (tk - 273.15) / (tk - 32.18)
        es = 6.1121 * math.exp(17.502 * y)
        # Apply "enhancement factor" to correct estimate for moist air:
        es = (1.0007 + (3.46e-6 * Pair)) * es 
    else:			# over ice
        y = (tk - 273.15)/(tk - 0.6)
        es = 6.1115 * math.exp(22.452 * y)
        es = (1.0003 + (4.18e-6 * Pair)) * es

    return es
