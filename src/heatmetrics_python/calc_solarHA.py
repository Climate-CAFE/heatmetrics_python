import datetime
import math

def calc_solarHA(year, month, day, hour, lon):
    """Calculate solar hour angle

    To calculate the solar hour angle in degrees.

    :param year: Year (4 digits)
    :type year: int
    :param month: Month (1-12)
    :type month: int
    :param day: Day of month (1-31)
    :type day: int
    :param hour: Hour (0-23 UTC)
    :type hour: int
    :param lon: Degrees east longitude (-180 to 180)
    :type lon: float
    :returns: the solar hour angle in degrees.
    :rtype: float
    :examples: calc_solarHA(2020, 7, 4, 12, -100)
    """

    # Calculate Julian Day; note index starts at 0
    #
    dt = datetime.datetime.strptime(f"{month:02d}-{day:02d}-{year:04d}", "%m-%d-%Y")
    jd = int(dt.strftime("%j")) - 1
 
    # Calculate angular fraction of the year in radians
    #
    g = ((2 * math.pi)/365.25) * (jd + (hour / 24))

    # Calculate the time correction, in radians
    #
    tc = (0.004297 + (0.107029 * math.cos(g)) - (1.837877 * math.sin(g)) -
           (0.837378 * math.cos(2*g)) - (2.340475 * math.sin(2*g)))

    # Calculate the solar hour angle, in degrees
    #
    sha = ((hour - 12) * 15) + lon + tc

    # Adjust the solar hour angle (sha), in degrees
    #
    if sha > 180:
        return sha - 360
    elif sha < -180:
        return sha + 360
    else:
        return sha
