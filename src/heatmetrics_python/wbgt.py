import numpy as np
from . import calc_solar_parameters
from .calc_solar_parameters import calc_solar_parameters
from . import stab_srdt
from .stab_srdt import stab_srdt
from . import est_wind_speed
from .est_wind_speed import est_wind_speed
from . import Tglobe
from .Tglobe import Tglobe
from . import Twb
from .Twb import Twb

def wbgt(year, month, dday, lat, lon, solar, cza, fdir, pres, Tair, 
         relhum, speed, zspeed, dT, urban):
    """Wet-Bulb Globe Temperature (WBGT)

    Calculates the outdoor wet bulb-globe temperature (WBGT), which is the
    weighted sum of the dry-bulb air temperature (Ta), the globe temperature (Tg), and
    the natural wet bulb temperature (Tw):

    WBGT = (0.1 ⋅ Ta) + (0.7 ⋅ Tw) + (0.2 ⋅ Tg)

    The program predicts Tw and Tg using meteorological input data, and then combines
    the results to produce WBGT.

    Reference: Liljegren, et al. Modeling the Wet Bulb Globe Temperature Using
    Standard Meteorological Measurements. J. Occup. Environ. Hyg. 5, 645-655 (2008).
    https://doi.org/10.1080/15459620802310770

    :param year: 4-digit integer, e.g., 2007
    :type year: int
    :param month: Month (1-12) or month = 0 if reporting day as day of year
    :type month: int
    :param dday: Decimal day of month (1-31.96) -or- day of year (1-366.96), in UTC day-	fractions
    :type dday: float
    :param lat: Degrees north latitude (-90 to 90)
    :type lat: float
    :param lon: Degrees east longitude (-180 to 180)
    :type lon: float
    :param solar: Solar irradiance (W/m2)
    :type solar: float
    :param cza: Cosine solar zenith angle (0-1); use calc_cza_int() or 	calc_solar_parameters()$cza if cza is not known
    :type cza: float
    :param fdir: Fraction of surface solar radiation that is direct (0-1)
    :type fdir: float 
    :param pres: Barometric pressure in millibars (equivalent to hPa)
    :type pres: float
    :param Tair: Dry-bulb air temperature (deg. C)
    :type Tair: float
    :param relhum: Relative humidity (\%)
    :type relhum: float
    :param speed: Wind speed (m/s)
    :type speed: float
    :param zspeed: Height of wind-speed measurement, meters (typically 10m)
    :type zspeed: float
    :param dT: Vertical temperature difference (upper minus lower) in degrees Celsius
    :type dT: float
    :param urban: 1 for urban locations or 0 for non-urban locations
    :type urban: int
    :returns: the wet-bulb globe temperature in degrees C.
    :rtype: float
    :examples: wbgt(2020, 7, 4.5, 42.36, -71.06, 700, 0.5, 0.5, 1013, 30, 60, 2, 10, -0.052, 1)
    """

    inputs = [year, month, dday, lat, lon, solar, cza, fdir, pres, Tair, 
                  relhum, speed, zspeed, dT, urban]
    # Check for missing data and return NaN
    if (any(np.isnan(x) for x in inputs)) or (-999 in inputs):
        return np.nan

    # cza and fdir are assumed to be known. If they are not, set them to NaN here
    # and the calc_solar_parameters() function will calculate approximations of them
    #
    solar = calc_solar_parameters(year, month, dday, lat, lon, solar, cza, fdir)['solarRet'] # adjusted solar irradiance if out of bounds

    # *********************************************** #
    #  estimate the 2-meter wind speed, if necessary  #
    # *********************************************** #

    REF_HEIGHT = 2.0 # 2-meter reference height
    MINIMUM_SPEED = 0.5
    if(zspeed != REF_HEIGHT):
        if(cza > 0):
            daytime = True
        else:
            daytime = False
        stability_class = stab_srdt(daytime, speed, solar, dT)
        speed = est_wind_speed(speed, zspeed, stability_class, urban)
    else:
       speed <- max(speed, MINIMUM_SPEED) 

    # **************** #
    # Unit Conversions #
    # **************** #

    tk = Tair + 273.15 # deg. C to kelvin
    rh = 0.01 * relhum # relative humidity % to fraction

    #  *************************************************** #
    #  Calculate the globe (Tg), natural wet bulb (Tnwb),  #
    #  psychrometric wet bulb (Tpsy), and                  #
    #  outdoor wet bulb globe temperatures (Twbg)          #
    #  *************************************************** #

    Tg = Tglobe(tk, rh, pres, speed, solar, fdir, cza)
    Tnwb = Twb(tk, rh, pres, speed, solar, fdir, cza)
    Twbg = (0.1 * Tair) + (0.2 * Tg) + (0.7 * Tnwb)

    return Twbg


