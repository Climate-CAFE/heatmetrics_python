import math

def dew_point(e, phase, Pair):
    """Calculate dew-point temperature from pressure

    Calculates the dew point or frost point temperature
    in units of Kelvin (K) from barometric pressure and vapor pressure. To calculate
    dew-point temperature from ambient temperature and relative humidity, use
    the td() function.

    :param e: Vapor pressure in millibars (equivalent to hPa)
    :type e: float
    :param phase: Indicator - 0 for dew point or 1 for frost point
    :type phase: int
    :param Pair: Barometric pressure in millibars (equivalent to hPa)
    :type Pair: float
    :returns: the dew-point temperature in units of Kelvin (K)
    :rtype: float
    :examples: dew_point(10, 0, 1014)
    """

    if phase == 0:   # Dew point
        # Calculate same enhancement factor as in function for saturation vapor pressure
        EF = 1.0007 + (3.46e-6 * Pair)
        z = math.log(e / (6.1121 * EF))
        tdk = 273.15 + 240.97 * z / (17.502 - z)
    else:	            # Frost point
        EF = 1.0003 + (4.18e-6 * Pair)
        z = math.log( e / (6.1115 * EF) )
        tdk = 273.15 + 272.55 * z / (22.452 - z)

    return tdk
