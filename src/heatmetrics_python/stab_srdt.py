import numpy as np

def stab_srdt(daytime, speed, solar, dT):
    """Stability class

    Estimates the stability class for calculating 2-meter wind
    speed from higher-altitude wind speeds.

    :param daytime: "1" for daytime, "0" for nighttime
    :type daytime: int
    :param speed: Wind speed (m/s)
    :type speed: float
    :param solar: Irradiance (W/m2)
    :type solar: float
    :param dT: Temperature differential between wind-speed heights (deg C)
    :type dT: float
    :returns: the stability class (0-6) used for adjusting wind speeds from
	    reference height to 2-meter height.
    :rtype: float
    :examples: stab_srdt(1, 3, 700, -0.052)
    """

    lsrdt = np.zeros((6, 8))
    lsrdt[0,] = [1, 1, 2, 4, 0, 5, 6, 0]
    lsrdt[1,] = [1, 2, 3, 4, 0, 4, 5, 0]  # CORRECTED columns 6 & 7 from "5, 6" to "4, 5"
    lsrdt[2,] = [2, 2, 3, 4, 0, 4, 4, 0]
    lsrdt[3,] = [3, 3, 4, 4, 0, 0, 0, 0]
    lsrdt[4,] = [3, 4, 4, 4, 0, 0, 0, 0]
    lsrdt[5,] = [0, 0, 0, 0, 0, 0, 0, 0]

    if daytime == 1: 
        if solar >= 925.0:
            j = 1 
        else:
            if solar >= 675.0:
                j = 2 
            else:
                if solar >= 175.0:
                    j = 3
                else:
                    j = 4
 
        if speed >= 6.0:
            i = 5
        else:
            if speed >= 5.0:
                i = 4
            else:
                if speed >= 3.0:
                    i = 3 
                else:
                    if speed >= 2.0:
                        i = 2
                    else: 
                        i = 1
    else:    # NOT daytime
        if dT >= 0.0:
            j = 7 
        else:
            j = 6

        if speed >= 2.5:
            i = 3
        else:
            if speed >= 2.0:
                i = 2 
            else:
                i = 1 

    return lsrdt[i-1][j-1]


