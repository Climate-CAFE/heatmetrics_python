import numpy as np

def utci(Tair, e, es, ws, D_Tmrt):
    """Universal Thermal Climate Index (UTCI)

    Calculates the universal thermal climate index (UTCI) from
    ambient temperature (deg C), vapor pressure (kPa), 10-meter wind speed (m/s),
    and mean radiant temperature (deg C). This regression approximation comes from
    Brode et al. (2011), https://doi.org/10.1007/s00484-011-0454-1

    :param Tair: Ambient temperature (deg C), between -50 and +50 deg C
    :type Tair: float
    :param e: Vapor pressure (kPa), <5 kPa
    :type e: float
    :param es: Saturation vapor pressure (kPa)
    :type es: float
    :param ws: 10-meter wind speed (m/s), < 17 m/s
    :type ws: float
    :param D_Tmrt: Mean Radiant Temperature minus ambient temperature (deg C)
    :type D_Tmrt: float
    :returns: the approximate UTCI in degrees C.
    :rtype: float 
    :examples: utci(30, 2, 4, 2, 15)
    """

    # Function is only valid for particular ranges of values; return NaN if any
    # of the values fall outside these ranges.
    if Tair < -50 or Tair > 50 or e > 5:
        return np.nan
    if D_Tmrt < -30 or D_Tmrt > 70 or ws > 30.3:
        return np.nan

    # The regression is valid only for RH values from 5-100%. Brode et al. (2011)
    # recommends setting e values in instances where RH < 5% to the equivalent vapor
    # pressure that it would have if RH = 5% (i.e., set values assuming RH = 5%.)
    #
    rh = (e / es) * 100

    if rh < 5:
        e = es * 0.05
    
    utci_approx = (Tair + 
        ( 6.07562052E-01 ) +
  		( -2.27712343E-02 ) * Tair +
  		( 8.06470249E-04 ) * Tair*Tair +
  		( -1.54271372E-04 ) * Tair*Tair*Tair +
  		( -3.24651735E-06 ) * Tair*Tair*Tair*Tair +
  		( 7.32602852E-08 ) * Tair*Tair*Tair*Tair*Tair +
  		( 1.35959073E-09 ) * Tair*Tair*Tair*Tair*Tair*Tair +
  		( -2.25836520E+00 ) * ws +
  		( 8.80326035E-02 ) * Tair*ws +
  		( 2.16844454E-03 ) * Tair*Tair*ws +
  		( -1.53347087E-05 ) * Tair*Tair*Tair*ws +
  		( -5.72983704E-07 ) * Tair*Tair*Tair*Tair*ws +
  		( -2.55090145E-09 ) * Tair*Tair*Tair*Tair*Tair*ws +
  		( -7.51269505E-01 ) * ws*ws +
  		( -4.08350271E-03 ) * Tair*ws*ws +
  		( -5.21670675E-05 ) * Tair*Tair*ws*ws +
  		( 1.94544667E-06 ) * Tair*Tair*Tair*ws*ws +
  		( 1.14099531E-08 ) * Tair*Tair*Tair*Tair*ws*ws +
  		( 1.58137256E-01 ) * ws*ws*ws +
  		( -6.57263143E-05 ) * Tair*ws*ws*ws +
  		( 2.22697524E-07 ) * Tair*Tair*ws*ws*ws +
  		( -4.16117031E-08 ) * Tair*Tair*Tair*ws*ws*ws +
  		( -1.27762753E-02 ) * ws*ws*ws*ws +
  		( 9.66891875E-06 ) * Tair*ws*ws*ws*ws +
  		( 2.52785852E-09 ) * Tair*Tair*ws*ws*ws*ws +
  		( 4.56306672E-04 ) * ws*ws*ws*ws*ws +
  		( -1.74202546E-07 ) * Tair*ws*ws*ws*ws*ws +
  		( -5.91491269E-06 ) * ws*ws*ws*ws*ws*ws +
  		( 3.98374029E-01 ) * D_Tmrt +
  		( 1.83945314E-04 ) * Tair*D_Tmrt +
  		( -1.73754510E-04 ) * Tair*Tair*D_Tmrt +
  		( -7.60781159E-07 ) * Tair*Tair*Tair*D_Tmrt +
  		( 3.77830287E-08 ) * Tair*Tair*Tair*Tair*D_Tmrt +
  		( 5.43079673E-10 ) * Tair*Tair*Tair*Tair*Tair*D_Tmrt +
  		( -2.00518269E-02 ) * ws*D_Tmrt +
  		( 8.92859837E-04 ) * Tair*ws*D_Tmrt +
  		( 3.45433048E-06 ) * Tair*Tair*ws*D_Tmrt +
  		( -3.77925774E-07 ) * Tair*Tair*Tair*ws*D_Tmrt +
  		( -1.69699377E-09 ) * Tair*Tair*Tair*Tair*ws*D_Tmrt +
  		( 1.69992415E-04 ) * ws*ws*D_Tmrt +
  		( -4.99204314E-05 ) * Tair*ws*ws*D_Tmrt +
  		( 2.47417178E-07 ) * Tair*Tair*ws*ws*D_Tmrt +
  		( 1.07596466E-08 ) * Tair*Tair*Tair*ws*ws*D_Tmrt +
  		( 8.49242932E-05 ) * ws*ws*ws*D_Tmrt +
  		( 1.35191328E-06 ) * Tair*ws*ws*ws*D_Tmrt +
  		( -6.21531254E-09 ) * Tair*Tair*ws*ws*ws*D_Tmrt +
  		( -4.99410301E-06 ) * ws*ws*ws*ws*D_Tmrt +
  		( -1.89489258E-08 ) * Tair*ws*ws*ws*ws*D_Tmrt +
  		( 8.15300114E-08 ) * ws*ws*ws*ws*ws*D_Tmrt +
  		( 7.55043090E-04 ) * D_Tmrt*D_Tmrt +
  		( -5.65095215E-05 ) * Tair*D_Tmrt*D_Tmrt +
  		( -4.52166564E-07 ) * Tair*Tair*D_Tmrt*D_Tmrt +
  		( 2.46688878E-08 ) * Tair*Tair*Tair*D_Tmrt*D_Tmrt +
  		( 2.42674348E-10 ) * Tair*Tair*Tair*Tair*D_Tmrt*D_Tmrt +
  		( 1.54547250E-04 ) * ws*D_Tmrt*D_Tmrt +
  		( 5.24110970E-06 ) * Tair*ws*D_Tmrt*D_Tmrt +
  		( -8.75874982E-08 ) * Tair*Tair*ws*D_Tmrt*D_Tmrt +
  		( -1.50743064E-09 ) * Tair*Tair*Tair*ws*D_Tmrt*D_Tmrt +
  		( -1.56236307E-05 ) * ws*ws*D_Tmrt*D_Tmrt +
  		( -1.33895614E-07 ) * Tair*ws*ws*D_Tmrt*D_Tmrt +
  		( 2.49709824E-09 ) * Tair*Tair*ws*ws*D_Tmrt*D_Tmrt +
  		( 6.51711721E-07 ) * ws*ws*ws*D_Tmrt*D_Tmrt +
  		( 1.94960053E-09 ) * Tair*ws*ws*ws*D_Tmrt*D_Tmrt +
  		( -1.00361113E-08 ) * ws*ws*ws*ws*D_Tmrt*D_Tmrt +
  		( -1.21206673E-05 ) * D_Tmrt*D_Tmrt*D_Tmrt +
  		( -2.18203660E-07 ) * Tair*D_Tmrt*D_Tmrt*D_Tmrt +
  		( 7.51269482E-09 ) * Tair*Tair*D_Tmrt*D_Tmrt*D_Tmrt +
  		( 9.79063848E-11 ) * Tair*Tair*Tair*D_Tmrt*D_Tmrt*D_Tmrt +
  		( 1.25006734E-06 ) * ws*D_Tmrt*D_Tmrt*D_Tmrt +
  		( -1.81584736E-09 ) * Tair*ws*D_Tmrt*D_Tmrt*D_Tmrt +
  		( -3.52197671E-10 ) * Tair*Tair*ws*D_Tmrt*D_Tmrt*D_Tmrt +
  		( -3.36514630E-08 ) * ws*ws*D_Tmrt*D_Tmrt*D_Tmrt +
  		( 1.35908359E-10 ) * Tair*ws*ws*D_Tmrt*D_Tmrt*D_Tmrt +
  		( 4.17032620E-10 ) * ws*ws*ws*D_Tmrt*D_Tmrt*D_Tmrt +
  		( -1.30369025E-09 ) * D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt +
  		( 4.13908461E-10 ) * Tair*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt +
  		( 9.22652254E-12 ) * Tair*Tair*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt +
  		( -5.08220384E-09 ) * ws*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt +
  		( -2.24730961E-11 ) * Tair*ws*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt +
  		( 1.17139133E-10 ) * ws*ws*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt +
  		( 6.62154879E-10 ) * D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt +
  		( 4.03863260E-13 ) * Tair*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt +
  		( 1.95087203E-12 ) * ws*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt +
  		( -4.73602469E-12 ) * D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt +
  		( 5.12733497E+00 ) * e +
  		( -3.12788561E-01 ) * Tair*e +
  		( -1.96701861E-02 ) * Tair*Tair*e +
  		( 9.99690870E-04 ) * Tair*Tair*Tair*e +
  		( 9.51738512E-06 ) * Tair*Tair*Tair*Tair*e +
  		( -4.66426341E-07 ) * Tair*Tair*Tair*Tair*Tair*e +
  		( 5.48050612E-01 ) * ws*e +
  		( -3.30552823E-03 ) * Tair*ws*e +
  		( -1.64119440E-03 ) * Tair*Tair*ws*e +
  		( -5.16670694E-06 ) * Tair*Tair*Tair*ws*e +
  		( 9.52692432E-07 ) * Tair*Tair*Tair*Tair*ws*e +
  		( -4.29223622E-02 ) * ws*ws*e +
  		( 5.00845667E-03 ) * Tair*ws*ws*e +
  		( 1.00601257E-06 ) * Tair*Tair*ws*ws*e +
  		( -1.81748644E-06 ) * Tair*Tair*Tair*ws*ws*e +
  		( -1.25813502E-03 ) * ws*ws*ws*e +
  		( -1.79330391E-04 ) * Tair*ws*ws*ws*e +
  		( 2.34994441E-06 ) * Tair*Tair*ws*ws*ws*e +
  		( 1.29735808E-04 ) * ws*ws*ws*ws*e +
  		( 1.29064870E-06 ) * Tair*ws*ws*ws*ws*e +
  		( -2.28558686E-06 ) * ws*ws*ws*ws*ws*e +
  		( -3.69476348E-02 ) * D_Tmrt*e +
  		( 1.62325322E-03 ) * Tair*D_Tmrt*e +
  		( -3.14279680E-05 ) * Tair*Tair*D_Tmrt*e +
  		( 2.59835559E-06 ) * Tair*Tair*Tair*D_Tmrt*e +
  		( -4.77136523E-08 ) * Tair*Tair*Tair*Tair*D_Tmrt*e +
  		( 8.64203390E-03 ) * ws*D_Tmrt*e +
  		( -6.87405181E-04 ) * Tair*ws*D_Tmrt*e +
  		( -9.13863872E-06 ) * Tair*Tair*ws*D_Tmrt*e +
  		( 5.15916806E-07 ) * Tair*Tair*Tair*ws*D_Tmrt*e +
  		( -3.59217476E-05 ) * ws*ws*D_Tmrt*e +
  		( 3.28696511E-05 ) * Tair*ws*ws*D_Tmrt*e +
  		( -7.10542454E-07 ) * Tair*Tair*ws*ws*D_Tmrt*e +
  		( -1.24382300E-05 ) * ws*ws*ws*D_Tmrt*e +
  		( -7.38584400E-09 ) * Tair*ws*ws*ws*D_Tmrt*e +
  		( 2.20609296E-07 ) * ws*ws*ws*ws*D_Tmrt*e +
  		( -7.32469180E-04 ) * D_Tmrt*D_Tmrt*e +
  		( -1.87381964E-05 ) * Tair*D_Tmrt*D_Tmrt*e +
  		( 4.80925239E-06 ) * Tair*Tair*D_Tmrt*D_Tmrt*e +
  		( -8.75492040E-08 ) * Tair*Tair*Tair*D_Tmrt*D_Tmrt*e +
  		( 2.77862930E-05 ) * ws*D_Tmrt*D_Tmrt*e +
  		( -5.06004592E-06 ) * Tair*ws*D_Tmrt*D_Tmrt*e +
  		( 1.14325367E-07 ) * Tair*Tair*ws*D_Tmrt*D_Tmrt*e +
  		( 2.53016723E-06 ) * ws*ws*D_Tmrt*D_Tmrt*e +
  		( -1.72857035E-08 ) * Tair*ws*ws*D_Tmrt*D_Tmrt*e +
  		( -3.95079398E-08 ) * ws*ws*ws*D_Tmrt*D_Tmrt*e +
  		( -3.59413173E-07 ) * D_Tmrt*D_Tmrt*D_Tmrt*e +
  		( 7.04388046E-07 ) * Tair*D_Tmrt*D_Tmrt*D_Tmrt*e +
  		( -1.89309167E-08 ) * Tair*Tair*D_Tmrt*D_Tmrt*D_Tmrt*e +
  		( -4.79768731E-07 ) * ws*D_Tmrt*D_Tmrt*D_Tmrt*e +
  		( 7.96079978E-09 ) * Tair*ws*D_Tmrt*D_Tmrt*D_Tmrt*e +
  		( 1.62897058E-09 ) * ws*ws*D_Tmrt*D_Tmrt*D_Tmrt*e +
  		( 3.94367674E-08 ) * D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt*e +
  		( -1.18566247E-09 ) * Tair*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt*e +
  		( 3.34678041E-10 ) * ws*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt*e +
  		( -1.15606447E-10 ) * D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt*e +
  		( -2.80626406E+00 ) * e*e +
  		( 5.48712484E-01 ) * Tair*e*e +
  		( -3.99428410E-03 ) * Tair*Tair*e*e +
  		( -9.54009191E-04 ) * Tair*Tair*Tair*e*e +
  		( 1.93090978E-05 ) * Tair*Tair*Tair*Tair*e*e +
  		( -3.08806365E-01 ) * ws*e*e +
  		( 1.16952364E-02 ) * Tair*ws*e*e +
  		( 4.95271903E-04 ) * Tair*Tair*ws*e*e +
  		( -1.90710882E-05 ) * Tair*Tair*Tair*ws*e*e +
  		( 2.10787756E-03 ) * ws*ws*e*e +
  		( -6.98445738E-04 ) * Tair*ws*ws*e*e +
  		( 2.30109073E-05 ) * Tair*Tair*ws*ws*e*e +
  		( 4.17856590E-04 ) * ws*ws*ws*e*e +
  		( -1.27043871E-05 ) * Tair*ws*ws*ws*e*e +
  		( -3.04620472E-06 ) * ws*ws*ws*ws*e*e +
  		( 5.14507424E-02 ) * D_Tmrt*e*e +
  		( -4.32510997E-03 ) * Tair*D_Tmrt*e*e +
  		( 8.99281156E-05 ) * Tair*Tair*D_Tmrt*e*e +
  		( -7.14663943E-07 ) * Tair*Tair*Tair*D_Tmrt*e*e +
  		( -2.66016305E-04 ) * ws*D_Tmrt*e*e +
  		( 2.63789586E-04 ) * Tair*ws*D_Tmrt*e*e +
  		( -7.01199003E-06 ) * Tair*Tair*ws*D_Tmrt*e*e +
  		( -1.06823306E-04 ) * ws*ws*D_Tmrt*e*e +
  		( 3.61341136E-06 ) * Tair*ws*ws*D_Tmrt*e*e +
  		( 2.29748967E-07 ) * ws*ws*ws*D_Tmrt*e*e +
  		( 3.04788893E-04 ) * D_Tmrt*D_Tmrt*e*e +
  		( -6.42070836E-05 ) * Tair*D_Tmrt*D_Tmrt*e*e +
  		( 1.16257971E-06 ) * Tair*Tair*D_Tmrt*D_Tmrt*e*e +
  		( 7.68023384E-06 ) * ws*D_Tmrt*D_Tmrt*e*e +
  		( -5.47446896E-07 ) * Tair*ws*D_Tmrt*D_Tmrt*e*e +
  		( -3.59937910E-08 ) * ws*ws*D_Tmrt*D_Tmrt*e*e +
  		( -4.36497725E-06 ) * D_Tmrt*D_Tmrt*D_Tmrt*e*e +
  		( 1.68737969E-07 ) * Tair*D_Tmrt*D_Tmrt*D_Tmrt*e*e +
  		( 2.67489271E-08 ) * ws*D_Tmrt*D_Tmrt*D_Tmrt*e*e +
  		( 3.23926897E-09 ) * D_Tmrt*D_Tmrt*D_Tmrt*D_Tmrt*e*e +
  		( -3.53874123E-02 ) * e*e*e +
  		( -2.21201190E-01 ) * Tair*e*e*e +
  		( 1.55126038E-02 ) * Tair*Tair*e*e*e +
  		( -2.63917279E-04 ) * Tair*Tair*Tair*e*e*e +
  		( 4.53433455E-02 ) * ws*e*e*e +
  		( -4.32943862E-03 ) * Tair*ws*e*e*e +
  		( 1.45389826E-04 ) * Tair*Tair*ws*e*e*e +
  		( 2.17508610E-04 ) * ws*ws*e*e*e +
  		( -6.66724702E-05 ) * Tair*ws*ws*e*e*e +
  		( 3.33217140E-05 ) * ws*ws*ws*e*e*e +
  		( -2.26921615E-03 ) * D_Tmrt*e*e*e +
  		( 3.80261982E-04 ) * Tair*D_Tmrt*e*e*e +
  		( -5.45314314E-09 ) * Tair*Tair*D_Tmrt*e*e*e +
  		( -7.96355448E-04 ) * ws*D_Tmrt*e*e*e +
  		( 2.53458034E-05 ) * Tair*ws*D_Tmrt*e*e*e +
  		( -6.31223658E-06 ) * ws*ws*D_Tmrt*e*e*e +
  		( 3.02122035E-04 ) * D_Tmrt*D_Tmrt*e*e*e +
  		( -4.77403547E-06 ) * Tair*D_Tmrt*D_Tmrt*e*e*e +
  		( 1.73825715E-06 ) * ws*D_Tmrt*D_Tmrt*e*e*e +
  		( -4.09087898E-07 ) * D_Tmrt*D_Tmrt*D_Tmrt*e*e*e +
  		( 6.14155345E-01 ) * e*e*e*e +
  		( -6.16755931E-02 ) * Tair*e*e*e*e +
  		( 1.33374846E-03 ) * Tair*Tair*e*e*e*e +
  		( 3.55375387E-03 ) * ws*e*e*e*e +
  		( -5.13027851E-04 ) * Tair*ws*e*e*e*e +
  		( 1.02449757E-04 ) * ws*ws*e*e*e*e +
  		( -1.48526421E-03 ) * D_Tmrt*e*e*e*e +
  		( -4.11469183E-05 ) * Tair*D_Tmrt*e*e*e*e +
  		( -6.80434415E-06 ) * ws*D_Tmrt*e*e*e*e +
  		( -9.77675906E-06 ) * D_Tmrt*D_Tmrt*e*e*e*e +
  		( 8.82773108E-02 ) * e*e*e*e*e +
  		( -3.01859306E-03 ) * Tair*e*e*e*e*e +
  		( 1.04452989E-03 ) * ws*e*e*e*e*e +
  		( 2.47090539E-04 ) * D_Tmrt*e*e*e*e*e +
  		( 1.48348065E-03 ) * e*e*e*e*e*e)

    return utci_approx

