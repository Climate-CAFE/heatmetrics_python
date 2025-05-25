import math
import numpy as np
from . import calc_cza
from .calc_cza import calc_cza

def calc_cza_int(lat, lon, y, mon, d, hr):
    """Calculate the cosine solar zenith angle integrated over the hour

    To calculate the integrated cosine of solar zenith angle (cza) for an hour.
    The calc_cza() function can be used by itself instead, but it is less accurate for sunrise and sunset 
    hours. See Hogan and Hirahara (2016) [https://doi.org/10.1002/2015GL066868] and Di Napoli 
    (2020) [https://doi.org/10.1007/s00484-020-01900-5] for more details. This function is 
    only for use with hourly time steps.

    :param lat: Degrees north latitude (-90 to 90)
    :type lat: float
    :param lon: Degrees east longitude (-180 to 180)
    :type lon: float
    :param y: Year (four digits, e.g., 2020)
    :type y: int
    :param mon: Month (1-12)
    :type mon: int
    :param d: Day of month (whole number)
    :type d: int
    :param hr: Hour (0-24 UTC)
    :type hr: int
    :returns: the integrated cosine of the solar zenith angle (cza).
    :rtype: float
    :examples: calc_cza_int(30, -100, 2020, 1, 1, 12)
    """

    E = [-math.sqrt(3.0 / 5.0), 0.0, math.sqrt(3.0 / 5.0)]
    W = [(5.0 / 9.0), (8.0 / 9.0), (5.0 / 9.0)]

    tbegin = -1
    tend = 1
    intervals_per_hour = 1

    nsplits = (tend - tbegin) * intervals_per_hour

    time_steps = np.append(np.arange(tbegin, tend), tend)

    integral = lat * 0

    for s in range(len(time_steps) - 1): 
        ti = time_steps[s]
        tf = time_steps[s + 1]
        deltat = tf - ti
        jacob = deltat / 2
        w = jacob * np.array(W)           # note case sensitivity of w
        t = jacob * np.array(E)
        t = t + ((tf + ti) / 2)

        for n in range(len(w)):
            cza = calc_cza(lat = lat,
                           lon = lon,
                           y = y,
                           mon = mon,
                           d = d,
                           hr = hr + t[n])
            integral = integral + w[n] * cza
    
    return integral / 2
