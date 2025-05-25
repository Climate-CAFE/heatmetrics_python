import math

def td(t, RH):
    """Calculate dew point temperature from T & RH

    Calculates the dew point temperature (Td)
    for a given ambient temperature and relative
    humidity. At saturation (100\% RH), Td = T. For all
    other RH, Td < T.

    Reference: Eqn. 8 in Lawrence (2005, p.226), https://doi.org/10.1175/BAMS-86-2-225

    :param t: temperature (*C)
    :type t: float
    :param RH: relative humidity (\%)
    :type RH: float
    :returns: the dewpoint temperature (*C)
    :rtype: float
    :examples: td(30, 70)
    """

    # Constants
    a1 = 17.625 # dimensionless
    b1 = 243.04 # *C

    td = ((b1 * (math.log(RH / 100) + ((a1 * t) / (b1 + t)))) /
           (a1 - math.log(RH / 100) - ((a1 * t) / (b1 + t))))

    return td

