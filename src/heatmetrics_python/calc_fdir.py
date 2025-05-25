import math
from . import solarposition
from .solarposition import solarposition

def calc_fdir(year, month, day, lat, lon, solar, cza):
    """Calculate fraction of solar irradiance due to direct beam (FDIR)

    To calculate the fraction of the solar irradiance due to the direct beam.

    :param year: Year (4 digits)
    :type year: int
    :param month: Month (1-12)
    :type month: int
    :param day: Day-fraction of month based on UTC time. Day number must include
	    fractional day based on time, e.g., 4.5 = noon UTC on the 4th of the month.
    :type day: float
    :param lat: Degrees north latitude (-90 to 90)
    :type lat: float
    :param lon: Degrees east longitude (-180 to 180)
    :type lon: float
    :param solar: Total surface solar irradiance (W/m2)
    :type solar: float
    :param cza: Cosine solar zenith angle (0-1)
    :type cza: float
    :returns: the fraction of irradiance due to direct beam ("fdir").
    :rtype: float
    :examples: calc_fdir(2020, 7, 4, 30, -100, 600, 0.5)
    """

    # DEFAULTS ____________________________________________________________________
    days_1900 = 0.0
    solarRet = solar
    fdir = 0

    # CONSTANTS ___________________________________________________________________
    SOLAR_CONST = 1367.0
    DEG_RAD = 0.017453292519943295
    CZA_MIN = 0.00873
    NORMSOLAR_MAX = 0.85

    solarposObj = solarposition(year, month, day, days_1900, lat, lon)
    elev = solarposObj['altitude']
    soldist = solarposObj['distance']

    toasolar = SOLAR_CONST * max(0, cza) / (soldist * soldist)

    #  If the sun is not fully above the horizon, then
    #  set the maximum (top of atmosphere [TOA]) solar = 0

    if cza < CZA_MIN:
        toasolar = 0 

    if toasolar > 0: 

        #  Account for any solar sensor calibration errors and
        #  make the solar irradiance consistent with normsolar

        normsolar = min(solar / toasolar, NORMSOLAR_MAX)
        solarRet = normsolar * toasolar

        #  calculate fraction of the solar irradiance due to the direct beam

        if normsolar > 0:
            fdir = math.exp(3 - 1.34 * normsolar - 1.65 / normsolar)
            fdir = max(min(fdir, 0.9), 0.0)
        else:
            fdir = 0
            cza = 0                       # added "cza <- 0"
    else:
        fdir = 0 
        cza = 0                          # added "cza <- 0"

    return fdir
