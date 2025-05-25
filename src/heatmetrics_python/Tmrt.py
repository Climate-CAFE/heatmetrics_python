import math

def Tmrt(SSRD, SSR, FDIR, STRD, STR, cza):
    """Mean radiant temperature

    To calculate the mean radiant temperature following the approach
    used by Di Napoli (2020), https://doi.org/10.1007/s00484-020-01900-5

    :param SSRD: Surface solar radiation downwards (W/m2) - direct + diffuse
    :type SSRD: float
    :param SSR: Surface net Solar Radiation (W/m2)
    :type SSR: float
    :param FDIR: Total sky direct solar radiation at the surface (W/m2)
    :type FDIR: float
    :param STRD: Surface thermal radiation downwards (W/m2)
    :type STRD: float
    :param STR: Surface net Thermal Radiation (W/m2)
    :type STR: float
    :param cza: Cosine of solar zenith angle (radians)
    :type cza: float
    :returns: the mean radiant temperature (K).
    :rtype: float
    """

    sigma = 5.67 * 10 ** (-8)  # Stefan-Boltzmann constant
    epsilon = 0.97          # emissivity of clothed human body (standard value)
    fa = 0.50               # angle factor
    alphaIR = 0.70          # absorption coefficient for body irradiation of solar radiation (standard value)

    dsw = SSRD - FDIR
    rsw = SSRD - SSR
    lur = STRD - STR

    # calculate fp projected factor area
    #
    gamma = math.asin(cza) * 180 / math.pi # in degrees
    fp = 0.308 * math.cos((math.pi / 180) * gamma * 0.998 - (gamma * gamma / 50000))

    if cza > 0.01:
        FDIR = FDIR / cza

    # calculate mean radiant temperature
    mrt = ((1 / sigma) *
            (fa * STRD +
               fa * lur +
               (alphaIR / epsilon) * (fa * dsw + fa * rsw + fp * FDIR))) ** 0.25

    return mrt
