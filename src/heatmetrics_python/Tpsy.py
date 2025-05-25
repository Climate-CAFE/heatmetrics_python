import math
from . import esat
from .esat import esat
from . import dew_point
from .dew_point import dew_point
from . import h_cylinder_in_air
from .h_cylinder_in_air import h_cylinder_in_air
from . import emis_atm
from .emis_atm import emis_atm
from . import viscosity
from .viscosity import viscosity
from . import diffusivity
from .diffusivity import diffusivity
from . import evap
from .evap import evap


def Tpsy(Tair, rh, Pair, speed, solar, fdir, cza):
    """Psychrometric wet-bulb temperature

    Calculates the psychrometric wet-bulb temperature.

    :param Tair: Air temperature (dry bulb) in Kelvin (K)
    :type Tair: float
    :param rh: Relative humidity as a proportion (0-1)
    :type rh: float
    :param Pair: Barometric pressure in millibars	(equivalent to hPa)
    :type Pair: float
    :param speed: Wind speed (m/s)
    :type speed: float
    :param solar: Solar irradiance (W/m2)
    :type solar: float
    :param fdir: Fraction of solar irradiance due to direct beam
    :type fdir: float
    :param cza: Cosine of solar zenith angle
    :type cza: float
    :returns: the psychrometric wet-bulb temperature in degrees Celsius
    :rtype: float
    :examples: Tpsy(293, 0.65, 1013, 4, 700, 0, -0.308)
    """

    rad = 0 # this is the only difference from the Twb() function

    # CONSTANTS ___________________________________________________________________
    CONVERGENCE = 0.02
    MAX_ITER = 100
    D_WICK = 0.007
    L_WICK = 0.0254
    PI = 3.1415926535897932
    Cp = 1003.5
    R_GAS = 8314.34
    M_AIR = 28.97
    M_H2O = 18.015
    R_AIR = (R_GAS / M_AIR)
    Pr = (Cp / (Cp + 1.25 * R_AIR))
    STEFANB = 5.6696e-8
    EMIS_SFC = 0.999
    EMIS_WICK = 0.95
    ALB_WICK = 0.4
    ALB_SFC = 0.45
    RATIO = (Cp * M_AIR / M_H2O)
    a = 0.56 # from Bedingfield and Drew
  
    # VARIABLES ___________________________________________________________________
    Tsfc = Tair
    sza = math.acos(cza)                 # solar zenith angle, radians
    eair = rh * esat(Tair, 0, Pair)
    Tdew = dew_point(eair, 0, Pair)  # needs Pair to calculate the enhancement factor
    Twb_prev = Tdew                      # first guess is the dew-point temperature
    converged = False
    iteration = 0

    while not converged:
        iteration = iteration + 1
        Tref = 0.5 * (Twb_prev + Tair)	# evaluate properties at the average temperature

        # Calculate convective heat transfer coefficient (h)
        h = h_cylinder_in_air(D_WICK, L_WICK, Tref, Pair, speed)

        # Calculate radiative heating term
        Fatm = STEFANB * EMIS_WICK * (0.5 * (emis_atm(Tair, rh, Pair) * (Tair ** 4) + EMIS_SFC * (Tsfc ** 4)) -
            (Twb_prev ** 4)) + (1 - ALB_WICK) * solar * ((1 - fdir) * (1 + 0.25 * D_WICK / L_WICK) +
            fdir * ((math.tan(sza) / PI) + 0.25 * D_WICK / L_WICK) + ALB_SFC)

        ewick = esat(Twb_prev, 0, Pair)
        density = Pair * 100 / (R_AIR * Tref)

        # Calculate Schmidt number (Sc)
        Sc = viscosity(Tref) / (density * diffusivity(Tref, Pair))

        Twb_new = Tair - evap(Tref) / RATIO * (ewick - eair) / (Pair - ewick) * ((Pr / Sc) ** a) + (Fatm / h * rad)
        
        if abs(Twb_new - Twb_prev) < CONVERGENCE:
            converged = True

        Twb_prev = 0.9 * Twb_prev + 0.1 * Twb_new

        if converged or iteration == MAX_ITER:
            break

    if converged:
        return Twb_new - 273.15
    else:
        return -9999

