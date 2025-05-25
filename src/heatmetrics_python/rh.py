import math
import numpy as np

def rh(t, q, p):
    """Calculate relative humidity (RH)

    Returns the relative humidity in percent (\%)

    :param t: temperature (*C)
    :type t: float
    :param q: specific humidity (kg/kg)
    :type q: float
    :param p: barometric pressure (Pa)
    :type p: float
    :returns: relative humidity (\%)
    :rtype: float
    :examples: rh(31, 0.0197, 101300)
    """

    # Constants
    a1 = 610.94 # Pa
    a2 = 17.625 # dimensionless
    a3 = 243.04 # *C

    # Saturation vapor pressure
    es = a1 * math.exp((a2 * t) / (a3 + t))

    RH = 100 * ((-q / ((q-1))) /
                 ((0.622 * es) / (p - es)))

    # Adjust for small excess at upper extreme,
    # otherwise return NaN
    if RH < 0 or RH > 105:
        return np.nan # Representing NA with NaN
    elif RH > 100:
        return 100
    else:
        return RH
  
 