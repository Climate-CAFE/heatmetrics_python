def daynum(year, month, day):
	"""Calculate day number of year

	Returns the sequential day number of a calendar date
	during a Gregorian calendar year (for years 1 onward). The integer arguments
	are the four-digit year, the month number, and the day of month number.
	(Jan. 1 = 01/01 = 001 Dec. 31 = 12/31 = 365 or 366.)
	A value of -1 is returned if the year is out of bounds.

	:param year: 4-digit year
	:type year: int
	:param month: Number of month (1-12)
	:type month: int
	:param day: Day of month
	:type day: int
	:returns: the day of year, i.e., "y-day" (1-366)
	:rtype: int
	:examples: daynum(2020, 7, 4)
	"""

	# There is no year 0 in the Gregorian calendar and the leap year cycle
	# changes for earlier years.
	if year < 1:
		return -1

	# Leap years (LY) are divisible by 4, except for centurial years not divisible by 400.
	# Examples of LY: 1996, 2000, 2004; 1896, *NOT* 1900, 1904
	# 1900 is NOT a leap year because it is a centurial year that is not divisible by 400, unlike 2000.
	leapyr = 0 # default is non-leap year
	if ((year % 4) == 0 and (year % 100) != 0) or ((year % 400) == 0):
		leapyr = 1 

	begmonth = [0,31,59,90,120,151,181,212,243,273,304,334]

	dnum = begmonth[month-1] + day
	if (leapyr == 1) & (month > 2):
		dnum = dnum + 1 

	return dnum