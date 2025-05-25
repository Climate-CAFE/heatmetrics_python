def est_wind_speed(speed, zspeed, stability_class, urban):
	"""Estimate 2-meter wind speeds

	Estimates 2-m wind speeds for all stability conditions when wind speeds are known
	at a different altitude. The minimum wind speed is set to 0.5 m/s.

	:param speed: Wind speed in meters per second (m/s)
	:type speed: float
	:param zspeed: Height of wind-speed measurement in meters (typically 10m)
	:type zspeed: float
	:param stability_class: Stability class (0-6), defined by the stab_srdt() function
	:type stability_class: float
	:param urban: Designation for whether area is urban (1) or not urban (0)
	:type urban: int 
	:returns: the estimated 2-meter wind speed in meters per second (m/s)
	:rtype: float
	:examples: est_wind_speed(2, 10, 2, 1)
	"""

	# Define constants:
	MIN_SPEED = 0.5   # 0.13 m/s in the original code
	REF_HEIGHT = 2.0

	urban_exp = [0.15, 0.15, 0.20, 0.25, 0.30, 0.30]
	rural_exp = [0.07, 0.07, 0.10, 0.15, 0.35, 0.55]

	if urban == 1:
		exponent = urban_exp[int(stability_class) - 1]
	else:
		exponent = rural_exp[int(stability_class) - 1] 

	est_speed = speed * ((REF_HEIGHT / zspeed) ** exponent)
	est_speed = max(est_speed, MIN_SPEED)
	return est_speed

