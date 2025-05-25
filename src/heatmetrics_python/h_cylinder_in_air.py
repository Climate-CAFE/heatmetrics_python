from . import viscosity
from .viscosity import viscosity
from . import thermal_cond
from .thermal_cond import thermal_cond

def h_cylinder_in_air(diameter, length, Tair, Pair, speed):
    """Convective heat transfer coefficient (cylinder)

    Calculates the convective heat transfer coefficient in
    units of W/(m2⋅K) for a long cylinder in cross flow.

    :param diameter: Cylinder diameter (m)
    :type diameter: float
    :param length: Cylinder length (m)
    :type length: float
    :param Tair: Air temperature (K)
    :type Tair: float
    :param Pair: Barometric pressure in millibars (equivalent to hPa)
    :type Pair: float
    :param speed: Wind speed (m/s)
    :type speed: float
    :returns: the convective heat transfer coefficient in units of W/(m2⋅K)
    :rtype: float
    :examples: h_cylinder_in_air(0.007, 0.0254, 290, 1014, 3)
    """

    # CONSTANTS ___________________________________________________________________
    a = 0.56
    b = 0.281
    c = 0.4
    R_GAS = 8314.34
    M_AIR = 28.97
    R_AIR = (R_GAS / M_AIR)
    MIN_SPEED = 0.5       # Originally was 0.13 m/s
    Cp = 1003.5
    Pr = (Cp / (Cp + 1.25 * R_AIR))

    density = Pair * 100 / (R_AIR * Tair)
    Re = max(speed, MIN_SPEED) * density * diameter / viscosity(Tair)
    Nu = b * (Re ** (1 - c)) * (Pr ** (1 - a))
    return Nu * thermal_cond(Tair) / diameter

