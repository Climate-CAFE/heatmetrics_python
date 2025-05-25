from . import viscosity
from .viscosity import viscosity
from . import thermal_cond
from .thermal_cond import thermal_cond
import math


def h_sphere_in_air(diameter, Tair, Pair, speed):
    """Convective heat transfer coefficient (sphere)

    To calculate the convective heat transfer coefficient
    in units of W/(m2⋅K) for flow around a sphere.

    :param diameter: Sphere diameter (m)
    :type diameter: float 
    :param Tair: Air temperature (K)
    :type Tair: float
    :param Pair: Barometric pressure in millibars (equivalent to hPa)
    :type Pair: float
    :param speed: Wind speed (m/s)
    :type speed: float
    :returns: the convective heat transfer coefficient in units of W/(m2⋅K)
    :rtype: float
    :examples: h_sphere_in_air(0.0508, 290, 1014, 3)
    """

    # CONSTANTS ___________________________________________________________________
    R_GAS = 8314.34
    M_AIR = 28.97
    R_AIR = (R_GAS / M_AIR)
    MIN_SPEED = 0.5   # originally was 0.13 m/s
    Cp = 1003.5
    Pr = (Cp / (Cp + 1.25 * R_AIR))

    density = Pair * 100 / ( R_AIR * Tair )

    # Calculate Reynolds Number (Re)
    Re = max(speed, MIN_SPEED) * density * diameter / viscosity(Tair)

    # Calculate Nusselt Number (Nu)
    Nu = 2.0 + 0.6 * math.sqrt(Re) * (Pr ** 0.3333)

    return Nu * thermal_cond(Tair) / diameter


