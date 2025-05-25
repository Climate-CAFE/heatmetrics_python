import numpy as np
import math
from . import solarposition
from .solarposition import solarposition


def calc_solar_parameters(year, month, day, lat, lon, solar, cza, fdir):
    """Calculate solar parameters

    To calculate the adjusted surface solar irradiance, cosine of the solar
    zenith angle, and fraction of the solar irradiance due to the direct beam. Note that
    calc_cza_int() provides more-accurate cza on hourly data and should be used when possible.

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
    :param cza: Cosine solar zenith angle (0-1); optional (supply "NA" if unknown)
    :type cza: float
    :param fdir: Fraction of the surface solar radiation from direct (0-1); optional (supply "NA" if unknown)
    :type fdir: float
    :returns: a dictionary of outputs: adjusted solar radiation ("solarRet"), cosine of the solar zenith angle ("cza", unchanged if user-supplied), and the fraction of irradiance due to direct beam ("fdir", unchanged if user-supplied).
    :rtype: dict
    :examples: calc_solar_parameters(2020, 7, 4, 30, -100, 600, 0.5, 0.5)
    """

    # DEFAULTS ____________________________________________________________________
    days_1900 = 0.0
    solarRet = solar

    # CONSTANTS ___________________________________________________________________
    SOLAR_CONST = 1367.0
    DEG_RAD = 0.017453292519943295
    CZA_MIN = 0.00873
    NORMSOLAR_MAX = 0.85

    solarposObj = solarposition(year, month, day, days_1900, lat, lon)
    ap_ra = solarposObj['ap_ra']
    ap_dec = solarposObj['ap_dec']
    elev = solarposObj['altitude']
    refr = solarposObj['refraction']
    azim = solarposObj['azimuth']
    soldist = solarposObj['distance']

    if np.isnan(cza):
        cza = math.cos((90 - elev) * DEG_RAD)  # if user does not supply cza

    toasolar = SOLAR_CONST * max(0, cza) / (soldist * soldist) # "Smax" in Liljegren (Eqn. 14, p. 648)

    cza = 0 if cza < 0 else cza   # Added this line

    #  If the sun is not fully above the horizon, then
    #  set the maximum (top of atmosphere [TOA]) solar = 0

    if cza < CZA_MIN:
        toasolar = 0 

    if toasolar > 0:
        #  Account for any solar sensor calibration errors and
        #  make the solar irradiance consistent with normsolar

        normsolar = min(solar / toasolar, NORMSOLAR_MAX )  # S* in Liljegren, Eqn. 13 (p. 648)
        solarRet = normsolar * toasolar

        #  calculate fraction of the solar irradiance due to the direct beam
        if normsolar > 0: 
            if np.isnan(fdir):
                fdir = math.exp(3 - 1.34 * normsolar - 1.65 / normsolar) 
            else:
                fdir = max(min(fdir, 0.9), 0.0)
        else:
            fdir = 0
            cza = 0                          # added "cza = 0"

    sp = {"solarRet": solarRet, "cza": cza, "fdir":fdir}
    return sp

