import datetime
import math
from . import calc_solarDA
from .calc_solarDA import calc_solarDA


def calc_cza(lat, lon, y, mon, d, hr):
    """Calculate the cosine of the solar zenith angle

    This function can be used by itself, but a more-accurate cza will
    be obtained with calc_cza_int(), which calls this function and integrates over the hour.

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
    :returns: cosine of the solar zenith angle (cza)
    :rtype: float
    :examples: calc_cza(30, -100, 2020, 1, 1, 12)
    """

    dt = datetime.datetime.strptime(f"{y:04d}-{mon:02d}-{d:02d}",
                                    "%Y-%m-%d") + datetime.timedelta(hours=hr)
 
    # Calculate Julian Day; note index starts at 0 - add 1 so that Jan. 1 = 1.
    #
    jd = int(dt.strftime("%j"))

    if hr < 0:
        hr = 24 + hr

    # declination angle + time correction for solar angle
    d_tc = calc_solarDA(jd, hr)
    d = d_tc['d']
    tc = d_tc['tc']

    d_rad = d * (math.pi / 180)

    lat_rad = lat * (math.pi / 180)

    sindec_sinlat = math.sin(d_rad) * math.sin(lat_rad)
    cosdec_coslat = math.cos(d_rad) * math.cos(lat_rad)

    # solar hour angle [h.deg]
    sha_rad = ((hr - 12) * 15 + lon + tc) * (math.pi / 180)
    csza = sindec_sinlat + cosdec_coslat * math.cos(sha_rad)

    if csza < 0:
        csza = 0

    return csza

