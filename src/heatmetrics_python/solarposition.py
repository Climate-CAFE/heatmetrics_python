import math
from . import daynum 
from .daynum import daynum


def solarposition(year, month, day, days_1900, latitude, longitude):
    """Solar position

    Calculates the Sun's apparent right ascension, apparent declination,
    altitude, atmospheric refraction correction applicable to the altitude, azimuth,
    and distance from Earth using the Astronomical Almanac of 1990, which is applicable
    for years 1950 - 2050, with an accuracy of 0.1 arc minutes for refraction at altitudes
    of at least 15 degrees.

    :param year: Four-digit year (Gregorian calendar). Use "0" if
	    reporting date as days since 1900
    :type year: int
    :param month: Month number (1-12). Use "0" if reporting date
	    as year and day of year (yday) -or- days since 1900
    :type month: int
    :param day: Fractional day of month (0-32) or day of year (0-367)
    :type day: float
    :param days_1900: Days since 1 January 1900 at 00:00:00 UTC
	    Use "0" if entering date as year, month, and day -or- year & yday
    :type days_1900: int
    :param latitude: Degrees north latitude (-90 to 90)
    :type latitude: float
    :param longitude: Degrees east longitude (-180 to 180)
    :type longitude: float 
    :returns: a dictionary containing apparent solar right ascension ("ap_ra"),
	    apparent solar declination ("ap_dec"), solar altitude ("altitude"), refraction
	    correction ("refraction"), solar azimuth ("azimuth"), and distance of Sun from
	    Earth ("distance")
    :rtype: dict
    :examples: solarposition(2020, 7, 4, 0, 42.36, -71.06)
    """

    # INPUTS ___________________________________________________________________
    # year       | Four-digit year (Gregorian calendar).
    #            |      * [1950 through 2049; 0 o.k. if using days_1900]
    # month      | Month number
    #            |    * [1 through 12; 0 o.k. if using daynumber for day]
    # day        | Calendar day.fraction, or daynumber.fraction.
    #            |      * If month is NOT 0: 0 through 32; 31st @ 18:10:00 UT = 31.75694
    #            |      * If month IS 0:     0 through 367; 366 @ 18:10:00 UT = 366.75694
    # days_1900  |  Days since 1900 January 0 @ 00:00:00 UT.
    #            |      * 18262.0 (1950/01/00) through 54788.0 (2049/12/32)
    #            |      * 1990/01/01 @ 18:10:00 UT = 32873.75694
    #            |      * 0.0 o.k. if using {year, month, day} or
    #            |    * {year, daynumber}
    # latitude   |  Observation site geographic latitude.
    #            |      * degrees.fraction, North positive
    # longitude  |Observation site geographic longitude.
    #            |      * degrees.fraction, East positive

    # OUTPUTS ___________________________________________________________________
    # ap_ra      | Apparent solar right ascension.
    #            |      * hours 0.0 <= *ap_ra < 24.0
    # ap_dec     |  Apparent solar declination.
    #            |      * degrees -90.0 <= *ap_dec <= 90.0
    # altitude   |  Solar altitude, uncorrected for refraction.
    #            |      * degrees -90.0 <= *altitude <= 90.0
    # refraction |  Refraction correction for solar altitude.
    #            |      * Add this to altitude to compensate for refraction.
    #            |      * degrees 0.0 <= *refraction
    # azimuth    |  Solar azimuth.
    #            |      *[degrees 0.0 <= *azimuth < 360.0, East is 90.0]
    # distance   |  Distance of Sun from Earth (heliocentric-geocentric).
    #            |      *[astronomical units; 1 a.u. is mean distance]
    # retValue   |  -1 if input parameters were out of bounds, or 0 if the function worked

    # DESCRIPTIONS _______________________________________________________________
    # daynumber       | Sequential daynumber during a year.
    # delta_days      | Whole days since 2000 January 0.
    # delta_years     | Whole years since 2000.
    # cent_J2000      | Julian centuries since epoch J2000.0 at 0h UT.
    # cos_alt         | Cosine of the altitude of Sun.
    # cos_apdec       | Cosine of the apparent declination of Sun.
    # cos_az          | Cosine of the azimuth of Sun.
    # cos_lat         | Cosine of the site latitude.
    # cos_lha         | Cosine of the local apparent hour angle of Sun.
    # days_J2000      | Days since epoch J2000.0.
    # ecliptic_long   | Solar ecliptic longitude.
    # lmst            | Local mean sidereal time.
    # local_ha        | Local mean hour angle of Sun.
    # gmst0h          | Greenwich mean sidereal time at 0 hours UT.
    # integral        | Integral portion of double precision number.
    # mean_anomaly    | Earth mean anomaly.
    # mean_longitude  | Solar mean longitude.
    # mean_obliquity  | Mean obliquity of the ecliptic.
    # sin_apdec       | Sine of the apparent declination of Sun.
    # sin_az          | Sine of the azimuth of Sun.
    # sin_lat         | Sine of the site latitude.
    # tan_alt         | Tangent of the altitude of Sun.
    # ut              | UT hours since midnight.

    # CONSTANTS _______________________________________________________________
    temp = 15                    # Earth mean atmospheric temperature at sea level, deg C
    pressure = 1013.25               # Earth mean atmospheric pressure at sea level, hPa (equivalent to mb)
    PI = 3.1415926535897932
    TWOPI = 6.2831853071795864
    DEG_RAD = 0.017453292519943295  # pi/180
    RAD_DEG = 57.295779513082323    # 180/pi

    # Make the default return value -1
    retVal = -1

    #Check latitude and longitude for proper range before calculating dates.

    if (latitude < (-90)) or (latitude > 90) or (longitude < (-180)) or (longitude > 180):
        return retVal # default retVal is -1, indicating an error

    # If year is not zero then assume date is specified by year, month, day.
    # If year is zero then assume date is specified by days_1900.

    if year != 0:    # Assume date given by {year, month, day} or {year, 0, daynumber}

        if (year < 1950) or (year > 2049): 
            return retVal # year is out of bounds; retVal == -1

        if month != 0: 
            if (month < 1) or (month > 12) or (day < 0.0) or (day > 33.0):
                return retVal # retVal == -1
      
            daynumber = daynum(year, month, math.floor(day)) 
        else:
            if (day < 0.0) or (day > 368.0):
                return retVal # retVal is still -1
            daynumber = math.floor(day)

        # Construct Julian centuries since J2000 at 0 hours UT of date,
        # days.fraction since J2000, and UT hours.

        delta_years = year - 2000

        # delta_days is days from 2000/01/00 (1900's are negative).

        delta_days = math.floor(delta_years * 365 + delta_years / 4 + daynumber)
        if year > 2000:
            delta_days = delta_days + 1 # J2000 is 2000/01/01.5

        days_J2000 = delta_days - 1.5

        cent_J2000 = days_J2000 / 36525.0

        integral = math.floor(day)
        ut = day - integral

        days_J2000 = days_J2000 + ut
        ut = ut * 24.0 
    else: # Date given by days_1900, i.e., number of days since 1900
        # e.g., days_1900 is 18262 for 1950/01/00, and 54788 for 2049/12/32.
        # A.A. 1990, K2-K4.
        if (days_1900 < 18262.0) or (days_1900 > 54788.0):  # outside acceptable range of 1950-2049
            return retVal # retVal is still -1, i.e., error

        # Construct days.fraction since J2000, UT hours, and
        # Julian centuries since J2000 at 0 hours UT of date.
        # days_1900 is 36524 for 2000/01/00. J2000 is 2000/01/01.5

        days_J2000 = days_1900 - 36525.5

        integral = math.floor(days_1900)
        ut = (days_1900 - integral) * 24

        cent_J2000 = (integral - 36525.5) / 36525.0

    # Compute solar position parameters.
    # A.A. (1990, C24)

    mean_anomaly = (357.528 + 0.9856003 * days_J2000)
    mean_longitude = (280.460 + 0.9856474 * days_J2000)

    # Put mean_anomaly and mean_longitude in the range 0 -> 2 pi (from degrees to radians)

    integral = math.floor(mean_anomaly / 360.0)
    mean_anomaly = (mean_anomaly / 360.0 - integral) * TWOPI
    integral = math.floor(mean_longitude / 360.0)
    mean_longitude = (mean_longitude / 360.0 - integral) * TWOPI

    mean_obliquity = (23.439 - 4.0e-7 * days_J2000) * DEG_RAD   # convert to radians
    ecliptic_long = ((1.915 * math.sin(mean_anomaly)) +
                      (0.020 * math.sin(2.0 * mean_anomaly))) * DEG_RAD + mean_longitude

    distance = 1.00014 - 0.01671 * math.cos(mean_anomaly) - 0.00014 * math.cos(2.0 * mean_anomaly)

    # Tangent of ecliptic_long separated into sine and cosine parts for ap_ra.

    ap_ra = math.atan2(math.cos(mean_obliquity) * math.sin(ecliptic_long), math.cos(ecliptic_long))

    # Change range of ap_ra from -pi -> pi to 0 -> 2 pi
    if ap_ra < 0.0:
        ap_ra = ap_ra + TWOPI

    # Put ap_ra in the range 0 -> 24 hours.
    integral = math.floor(ap_ra / TWOPI)
    ap_ra = (ap_ra / TWOPI - integral) * 24.0

    ap_dec = math.asin(math.sin(mean_obliquity) * math.sin(ecliptic_long))

    # Calculate local mean sidereal time.
    # A.A. 1990, B6-B7.

    # Horner's method of polynomial exponent expansion used for gmst0h.
    gmst0h = 24110.54841 + cent_J2000 * (8640184.812866 + cent_J2000 * (0.093104 - cent_J2000 * 6.2e-6))

    #Convert gmst0h from seconds to hours and put in the range 0 -> 24.
    #gmst0h = modf(gmst0h / 3600.0 / 24.0, &integral) * 24.0
    integral = math.floor(gmst0h/3600/24)
    if integral < 0:
        integral = integral + 1  # to match behavior of C modf() when dealing with negative numbers
    gmst0h = (gmst0h/3600/24 - integral) * 24

    if gmst0h < 0.0:
        gmst0h <- gmst0h + 24.0

    # Ratio of lengths of mean solar day to mean sidereal day is 1.00273790934
    # in 1990. Change in sidereal day length is < 0.001 second over a century.
    # A. A. 1990, B6.

    lmst = gmst0h + (ut * 1.00273790934) + longitude / 15.0

    # Put lmst in the range 0 -> 24 hours.
    integral = math.floor(lmst/24)
    if integral < 0:
        integral = integral + 1  # to match behavior of C modf()
    lmst = (lmst/24 - integral) * 24

    if lmst < 0.0:
        lmst = lmst + 24.0

    # Calculate local hour angle, altitude, azimuth, and refraction correction.
    # A.A. 1990, B61-B62

    local_ha = lmst - ap_ra

    # Put hour angle in the range -12 to 12 hours.
    if local_ha < (-12.0):
        local_ha = local_ha + 24.0
    else:
        if local_ha > 12.0:
            local_ha = local_ha - 24.0

    # Convert latitude and local_ha to radians
    latitude = latitude * DEG_RAD
    local_ha = local_ha / 24.0 * TWOPI

    cos_apdec = math.cos(ap_dec)
    sin_apdec = math.sin(ap_dec)
    cos_lat = math.cos(latitude)
    sin_lat = math.sin(latitude)
    cos_lha = math.cos(local_ha)

    altitude = math.asin(sin_apdec * sin_lat + cos_apdec * cos_lha * cos_lat)

    cos_alt = math.cos(altitude)

    # Avoid tangent overflow at altitudes of +-90 degrees.
    # 1.57079615 radians is equal to 89.99999 degrees.

    if abs(altitude) < 1.57079615:
        tan_alt = math.tan(altitude)
    else:
        tan_alt = 6.0e6

    cos_az = (sin_apdec * cos_lat - cos_apdec * cos_lha * sin_lat) / cos_alt
    sin_az = -(cos_apdec * math.sin(local_ha) / cos_alt)
    azimuth = math.acos(cos_az)

    #Change range of azimuth from 0 -> pi to 0 -> 2 pi
    if math.atan2(sin_az, cos_az) < 0.0:
        azimuth = TWOPI - azimuth

    # Convert ap_dec, altitude, and azimuth to degrees
    ap_dec = ap_dec * RAD_DEG
    altitude = altitude * RAD_DEG
    azimuth = azimuth * RAD_DEG

    # Compute refraction correction to be added to altitude to obtain actual position.
    # * Refraction calculated for altitudes of -1 degree or more allows for a
    # * pressure of 1040 mb and temperature of -22 C. Lower pressure and higher
    # * temperature combinations yield less than 1 degree refraction.
    # * NOTE:
    # * The two equations listed in the A.A. have a crossover altitude of
    # * 19.225 degrees at standard temperature and pressure. This crossover point
    # * is used instead of 15 degrees altitude so that refraction is smooth over
    # * the entire range of altitudes. The maximum residual error introduced by
    # * this smoothing is 3.6 arc seconds at 15 degrees. Temperature or pressure
    # * other than standard will shift the crossover altitude and change the error.

    if (altitude < (-1.0)) or (tan_alt == 6.0e6):
        refraction = 0.0
    else:
        if altitude < 19.225:
            refraction = (0.1594 + (altitude) * (0.0196 + 0.00002 * (altitude))) * pressure
            refraction = refraction / (1.0 + (altitude) * (0.505 + 0.0845 * (altitude))) * (273.0 + temp) 
        else:
            refraction = 0.00452 * (pressure / (273.0 + temp)) / tan_alt

    # To match Michalsky's sunae program, the following line was inserted
    # by JC Liljegren to add the refraction correction to the solar altitude

    altitude = altitude + refraction

    # If we made it here, then everything worked.
    retVal = 0

    outputs = {"retVal": retVal, "distance": distance, "azimuth": azimuth, "refraction": refraction,
               "altitude": altitude, "ap_dec": ap_dec, "ap_ra": ap_ra}
    return outputs

