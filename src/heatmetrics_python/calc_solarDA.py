import math

def calc_solarDA(jd, hour):
    """Calculate solar declination angle

    This function calculates the solar declination angle ("d") in degrees and time correction ("tc").

    :param jd: Julian day of year (1-366, e.g., Feb. 1 = 32)
    :type jd: int
    :param hour: Hour (0-23 UTC)
    :type hour: int
    :returns: a dictionary of outputs: solar declination angle ("d") and time offset ("tc").
    :rtype: dict
    :examples calc_solarDA(40, 12)
    """

    # Calculate angular fraction of the year in radians
    #
    g = (360 / 365.25) * (jd + (hour / 24))  # fractional year g in degrees
    
    if g > 360:
        g = g - 360

    g_rad =  g * (math.pi / 180) # convert to radians

    # Calculate the solar declination angle, lowercase delta, in degrees:
    #
    d = 0.396372 - 22.91327 * math.cos(g_rad) + 4.025430 * math.sin(g_rad) - 0.387205 * math.cos(2 * g_rad) + 0.051967 * math.sin(2 * g_rad) - 0.154527 * math.cos(3 * g_rad) + 0.084798 * math.sin(3 * g_rad)

    tc = (0.004297 + 0.107029 * math.cos(g_rad) - 1.837877 * math.sin(g_rad) -
           0.837378 * math.cos(2 * g_rad) - 2.340475 * math.sin(2 * g_rad))

    outputs = {"d": d, "tc": tc}
  
    return outputs