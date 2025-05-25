import numpy as np
from . import h_sphere_in_air
from .h_sphere_in_air import h_sphere_in_air
from . import emis_atm
from .emis_atm import emis_atm


def Tglobe(Tair, rh, Pair, speed, solar, fdir, cza):
    """Globe temperature

    Calculates the globe temperature as an input to the wet-bulb
    globe temperature (WBGT).

    :param Tair: Dry-bulb air temperature (Kelvin)
    :type Tair: float
    :param rh: Relative humidity as proportion (0-1)
    :type rh: float
    :param Pair: Barometric pressure in millibars (equivalent to hPa)
    :type Pair: float
    :param speed: Wind speed (m/s)
    :type speed: float
    :param solar: Solar irradiance (W/m2)
    :type solar: float
    :param fdir: Fraction of solar irradiance due to direct beam (0-1)
    :type fdir: float 
    :param cza: Cosine of solar zenith angle (0-1)
    :type cza: float
    :returns: the globe temperature in degrees Celsius
    :examples: Tglobe(290, 0.75, 1014, 3, 700, 0.32, 0.96)
    """

    # The equation for Tglobe_new has cza in the denominator, so it will result in
    # NaN for cza = 0. This should only be 0 at nighttime, in which case both fdir
    # and cza should both be zero. When fdir and cza are both 0, the value of cza
    # has no bearing on Tglobe, even when solar > 0. To avoid an
    # unnecessary NaN value, replace cza with 0.01 when cza < 0.01

    if cza < 0.01:
        cza = 0.01

    # CONSTANTS ______________________________________________________________________
    EMIS_GLOBE = 0.95
    ALB_GLOBE = 0.05
    ALB_SFC = 0.45
    D_GLOBE = 0.0508
    EMIS_SFC = 0.999
    STEFANB = 5.6696e-8
    CONVERGENCE = 0.02
    MAX_ITER = 100    # Increased from 50; adds to processing time but reduces missingness

    # VARIABLES ______________________________________________________________________
    Tsfc = Tair
    Tglobe_prev = Tair # first guess is the air temperature
    converged = False
    iteration = 0

    while not converged: 
        iteration = iteration + 1
        Tref = 0.5 * (Tglobe_prev + Tair)	# evaluate properties at the average temperature
        h = h_sphere_in_air(D_GLOBE, Tref, Pair, speed)

        Tglobe_new = (0.5 * (emis_atm(Tair, rh, Pair) * (Tair ** 4) + EMIS_SFC * (Tsfc ** 4)) -
                  h / (STEFANB * EMIS_GLOBE) * (Tglobe_prev - Tair) +
                  solar / (2 * STEFANB * EMIS_GLOBE) * (1 - ALB_GLOBE) *
                  (fdir * (1 / (2 * cza) - 1) + 1 + ALB_SFC)) ** 0.25

        if abs(Tglobe_new - Tglobe_prev) < CONVERGENCE:
            converged = True

        Tglobe_prev = 0.9 * Tglobe_prev + 0.1 * Tglobe_new

        if (converged) | (iteration == MAX_ITER):
            break
 
    if converged:
        return Tglobe_new - 273.15
    else:
        return np.nan
