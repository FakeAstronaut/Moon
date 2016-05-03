# coding: utf-8

#Position of the moon
#######
########

import calendar
import math
import datetime
import leapseconds #from https://github.com/eggert/tz/blob/master/leap-seconds.list
#import turtle
#import numpy

#Constants
pi 								= 3.1415927
daysinmonth						= [31,28,31,30,31,30,31,31,30,31,30,31]
##sun
Ecliptic_longitude 				= 279.403303  # at epoch 1990.0
Ecliptic_longitude_of_perigee 	= 282.768422
eccentricity_of_orbit 			= 0.016713
days_for_360 					= 365.242191
##moon
mean_longitude 					= 318.351648  #at epoch
mean_longitude_of_perigee 		= 36.340410   #at epoch
mean_longitude_of_node			= 318.510107  #at epoch
inclination_of_moon_orbit		= 5.145396
########
def adjustrange1(x):
	if x > 360:
		x -= 360*int(x/360)
	elif x < 0:
		x += 360*(abs(int(x/360))+1)
	return x

def adjustrange2(x):
	if x > 24:
		x -= 24*int(x/24)
	elif x < 0:
		x += 24*(abs(int(x/24))+1)
	return x	
	
def adjustrange3(x):
	if x > 180:
		x -= 180*int(x/180)
	elif x < 0:
		x += 180*(abs(int(x/360))+1)
	return x

def adjust_by_quadrant(x,y,tan_yx):
##		Ecliptic to equatorial coordinate conversion, pg 40
	if (x < 0) and (y > 0):
		if tan_yx > 180:
			tan_yx -= 180*int(tan_yx/180)
		elif tan_yx < 90:
			tan_yx += 180*(abs(int(tan_yx/180))+1)
	elif (x > 0) and (y > 0):
		if tan_yx > 90:
			tan_yx -= 180*int(tan_yx/180)
		elif tan_yx < 0:
			tan_yx += 180*(abs(int(tan_yx/180))+1)
	elif (x > 0) and (y < 0):
		if tan_yx > 0:
			tan_yx -= 180*int(tan_yx/180)
		elif tan_yx < -90:
			tan_yx += 180*(abs(int(tan_yx/180))+1)
	elif (x < 0) and (y < 0):
		if tan_yx > -90:
			tan_yx -= 180*int(tan_yx/180)
		elif tan_yx < -180:
			tan_yx += 180*(abs(int(tan_yx/180))+1)	
	return tan_yx
	
def decdeg2dms(dd):
	negative = dd < 0
	dd = abs(dd)
	minutes,seconds = divmod(dd*3600,60)
	degrees,minutes = divmod(minutes,60)
	if negative:
		if degrees > 0:
			degrees = -degrees
		elif minutes > 0:
			minutes = -minutes
		else:
			seconds = -seconds
	return (degrees,minutes,seconds)
	
def dayfraction_to_hms(x):
	x = abs(x)
	hours = int(x * 24)
	minutes = int(((time_as_frac_of_day * 24) - hours )* 60)
	seconds = int((((time_as_frac_of_day * 24) - hours )* 60 - minutes) * 60)
	return (hours,minutes,seconds)
##########

#day=26
#month=2
#year=1979
#timeH=16
#timeM=0
#timeS=0
#observer_latitude = 53.3478 ## N or S
#observer_longitude = -6.2597 ##negative means W, positive E
def calculate_all(day=26,month=2,year=1979,timeH=16,timeM=0,timeS=0,observer_latitude = 53.3478,observer_longitude = -6.2597):	
	print "Calculated with set date: "+str(day)+"/"+str(month)+"/"+str(year)+"/ at " + str(timeH)+":"+str(timeM)+":"+str(timeS)+".\n"

	## Step 1 - pg 144 ###############
	timeS+= 32.184 + leapseconds.dTAI_UTC_from_utc(datetime.datetime(year,month,day,timeH,timeM,timeS)).seconds #converting to Terrestrial Dynamic Time
	time_as_frac_of_day = ((timeS/60.0 + timeM)/60.0 + timeH)/24.0

	daystotal=0
	for monthdays in daysinmonth[:month-1]:
		daystotal += monthdays

	daystotal += day
	#print "Step 1 - d =",daystotal + time_as_frac_of_day
	####################################

	## Step 2 - pg 144 ###############
	total_days = (year-1990)*365 + calendar.leapdays(1990, year+1) + daystotal + time_as_frac_of_day
	#print "Step 2 - D =",total_days
	####################################

	## Step 3 - pg 144 ###############
	###		Step 3 = pg 88
	Mean_anomaly1 = (360/days_for_360 * total_days)
	Mean_anomaly1 = adjustrange1(Mean_anomaly1)
	###		##############
	###		Step 4 = pg 88
	Mean_anomaly2 = Mean_anomaly1 + Ecliptic_longitude - Ecliptic_longitude_of_perigee
	if Mean_anomaly2 < 0:
		Mean_anomaly2 += 360
	#print "Step 3 - M =",Mean_anomaly2  ##still step 3 on pg144
	###		##############
	###		Step 5 = pg 88
	E_c = (360.0/pi)* eccentricity_of_orbit * math.sin(math.radians(Mean_anomaly2))
	###		##############
	###		Step 6 = pg 88
	SunGeometricEclipticLongitude = Mean_anomaly1 + E_c + Ecliptic_longitude
	SunGeometricEclipticLongitude = adjustrange1(SunGeometricEclipticLongitude)
	#print "Step 3 - Lambda =",SunGeometricEclipticLongitude,"        M =",Mean_anomaly2
	###		##############
	######################################

	## Step 4 - pg 144 ##############
	l  = 13.1763966 * total_days + mean_longitude
	l = adjustrange1(l)
	#print "Step 4 - l =",l 
	######################################

	## Step 5 - pg 144 ##############
	M_m = l - 0.1114041 * total_days - mean_longitude_of_perigee
	M_m = adjustrange1(M_m)
	#print "Step 5 - M_m =",M_m 
	######################################

	## Step 6 - pg 144 ##############
	N = mean_longitude_of_node - 0.0529539 * total_days	
	N = adjustrange1(N)
	#print "Step 6 - N =",N 
	######################################

	## Step 7 - pg 144 ##############
	C 	= l - SunGeometricEclipticLongitude
	E_v = 1.2739 * math.sin(math.radians(2*C - M_m))	
	#print "Step 7 - E_v =",E_v 
	######################################

	## Step 8 - pg 144 ##############
	A_e = 0.1858 * math.sin(math.radians(Mean_anomaly2))
	A_3	= 0.37   * math.sin(math.radians(Mean_anomaly2))	
	#print "Step 8 - A_e =",A_e,"      A_3 =",A_3
	######################################

	## Step 9 - pg 144 ##############
	Corrected_anomaly = M_m + E_v - A_e - A_3			#M'_m
	#print "Step 9 - M\'_m =",Corrected_anomaly 
	######################################

	## Step 10 - pg 144 ##############
	E_c = 6.2886 * math.sin(math.radians(Corrected_anomaly))
	#print "Step 10 - E_c =",E_c 
	######################################

	## Step 11 - pg 144 ##############
	A_4 = 0.214 * math.sin(math.radians(2 * Corrected_anomaly))
	#print "Step 11 - A_4 =",A_4 
	######################################

	## Step 12 - pg 144 ##############
	l_prime = l + E_v + E_c - A_e + A_4
	#print "Step 12 - l\' =",l_prime 
	######################################

	## Step 13 - pg 144 ##############
	V = 0.6583 * math.sin(math.radians(2*(l_prime - SunGeometricEclipticLongitude)))
	#print "Step 13 - V =",V 
	######################################

	## Step 14 - pg 144 ##############
	true_longitude = l_prime + V		#l''= l' + V
	#print "Step 14 - l\'\' =",true_longitude 
	######################################

	## Step 15 - pg 144 ##############
	N_prime = N - 0.16 * math.sin(math.radians(Mean_anomaly2))
	#print "Step 15 - N\' =",N_prime 
	######################################

	## Step 16 - pg 144 ##############
	y = math.sin(math.radians(true_longitude - N_prime)) * math.cos(math.radians(inclination_of_moon_orbit))
	#print "Step 16 - y =",y
	######################################

	## Step 17 - pg 144 ##############
	x = math.cos(math.radians(true_longitude - N_prime))
	#print "Step 17 - x =",x 
	######################################

	## Step 18 - pg 144 ##############
	tan_yx = math.degrees(math.atan(y/x))
	#tan_yx = math.degrees(numpy.arctan(y/x))
	##		Ecliptic to equatorial coordinate conversion, pg 40
	tan_yx = adjust_by_quadrant(x,y,tan_yx)

	#print "Step 18 - tan_yx =",tan_yx
	######################################

	## Step 19 - pg 144 ##############
	lambda_m = tan_yx + N_prime
	#print "Step 19 - lambda_m =",lambda_m
	######################################

	## Step 20 - pg 144 ##############
	beta_m = math.degrees(math.asin(math.sin(math.radians(true_longitude - N_prime)) * math.sin(math.radians(inclination_of_moon_orbit))))
	#print "Step 20 - beta_m =",beta_m
	######################################

	## Step 21 - pg 144 ##############

	##			julian days
	###		Step 1 = pg 41
	####		Step 2 = pg 7

	if (month == 1) or (month == 2):
		year2 = year -1
		month2 = month +12
	else:
		year2 = year
		month2= month

	####		##############
	####		Step 3 = pg 7
	#if (year >= 1582) and (month >= 10) and (day >= 15):
	if datetime.datetime(year,month,day) >= datetime.datetime(1582,10,15):
		A = int(year2/100)
		B = 2 - A + int(A/4)
	else:
		B = 0

	####		##############
	####		Step 4 = pg 7
	if year2 > 0:
		C = int(365.25 * year2)
	else:
		C = int((365.25 * year2) - 0.75)

	####		##############
	####		Step 5 = pg 7
	D = int(30.6001 * (month2 +1))

	####		##############
	####		Step 6 = pg 7
	JD = B + C + D + day + 1720994.5 ##julian days
	###		##############

	#Calculating mean obliquity of the ecliptic
	###		Step 2 = pg 41
	JD -= 2451545
	###		##############
	###		Step 3 = pg 41
	T = JD/36525.0
	###		##############
	###		Step 4 = pg 41
	change_in_mean_obliquity_of_ecliptic = 46.815 * T + 0.0006*T*T - 0.00181*T*T*T
	###		##############
	###		Step 5 = pg 41
	change_in_mean_obliquity_of_ecliptic /= 3600.0 
	###		##############
	###		Step 6 = pg 41
	mean_obliquity_of_ecliptic = 23.439292 - change_in_mean_obliquity_of_ecliptic
	###		##############
	##
	## Formulas on pg 40
	alpha_m = math.degrees(math.atan((math.sin(math.radians(lambda_m)) * math.cos(math.radians(mean_obliquity_of_ecliptic)) - math.tan(math.radians(beta_m)) * math.sin(math.radians(mean_obliquity_of_ecliptic)))/math.cos(math.radians(lambda_m))))
	alpha_m = adjustrange1(alpha_m)
	alpha_m2 = decdeg2dms(alpha_m/15.0)
	print "--------------------------------------------------\n"
	print "Right ascension, alpha_m = {hours}h {minutes}m {seconds:.2f}s".format(hours=int(alpha_m2[0]), minutes=int(alpha_m2[1]), seconds=alpha_m2[2])

	delta_m = math.degrees(math.asin(math.sin(math.radians(beta_m)) * math.cos(math.radians(mean_obliquity_of_ecliptic)) + math.cos(math.radians(beta_m)) * math.sin(math.radians(mean_obliquity_of_ecliptic)) * math.sin(math.radians(lambda_m))))
	delta_m2 = decdeg2dms(delta_m)
	print u"Declination,     delta_m = {degrees}° {minutes}\' {seconds:.2f}\'\'".format(degrees=int(delta_m2[0]), minutes=str(int(delta_m2[1])).zfill(2), seconds=delta_m2[2])
	##
	######################################
	print "\n\n"
	print u"Calculated with observer coordinates: LAT "+str(observer_latitude)+u"° , LON "+ str(observer_longitude)+u"° .\n"
	##Converting to Horizontal coordinate system
	#Converting UT to GST pg17
	T0 = 6.697374558 + (2400.051336 * T) + (0.000025862 * T * T)

	T0 = adjustrange2(T0)

	UT = (timeS/60.0 + timeM)/60.0 + timeH

	UT *= 1.002737909

	GST = adjustrange2(UT + T0)
	###
	#Converting GST to LST pg20
	observer_longitude2 = observer_longitude/15.0

	# if observer_longitude2 < 0: ##check if west
		# LST = GST - observer_longitude2
	# elif observer_longitude2 > 0: ##check if east
		# LST = GST + observer_longitude2

	LST = GST + observer_longitude2
	if LST > 24:
		LST -=24
	elif LST < 0:
		LST += 24

	###
	##pg 36
	Hour_angle = adjustrange2(LST - alpha_m)

	Hour_angle2 = Hour_angle * 15.0 

	sin_altitude = math.sin(math.radians(delta_m)) * math.sin(math.radians(observer_latitude)) + math.cos(math.radians(delta_m)) * math.cos(math.radians(observer_latitude)) * math.cos(math.radians(Hour_angle2))

	altitude = math.degrees(math.asin(sin_altitude))

	cos_azimuth = (math.sin(math.radians(delta_m)) - math.sin(math.radians(observer_latitude)) * math.sin(math.radians(altitude))) / (math.cos(math.radians(observer_latitude)) * math.cos(math.radians(altitude)))

	azimuth_prime = math.degrees(math.acos(cos_azimuth))

	if math.sin(math.radians(Hour_angle2)) < 0:
		azimuth = azimuth_prime
	else:
		azimuth = 360 - azimuth_prime


	altitude2 = decdeg2dms(altitude)
	print "--------------------------------------------------\n"
	print u"altitude = {degrees}° {minutes}\' {seconds:.2f}\'\'".format(degrees=int(altitude2[0]), minutes=str(int(altitude2[1])).zfill(2), seconds=altitude2[2])
	azimuth2 = decdeg2dms(azimuth)
	print u"azimuth = {degrees}° {minutes}\' {seconds:.2f}\'\'".format(degrees=int(azimuth2[0]), minutes=str(int(azimuth2[1])).zfill(2), seconds=azimuth2[2])
	###################################################################

	##Calculating phase of the moon pg147
	##
	age_of_moon = true_longitude - SunGeometricEclipticLongitude
	phase_of_moon = 0.5 * (1 - math.cos(math.radians(age_of_moon)))
	print "--------------------------------------------------\n"
	print "The phase of the moon, as a percentage: "+str(round(phase_of_moon * 100,3))+"%.\n"
	###################################################################
	##the position angle of the moon bright limb pg149

	alpha_s = math.degrees(math.atan((math.sin(math.radians(SunGeometricEclipticLongitude)) * math.cos(math.radians(mean_obliquity_of_ecliptic)) - math.tan(math.radians(0)) * math.sin(math.radians(mean_obliquity_of_ecliptic)))/math.cos(math.radians(SunGeometricEclipticLongitude))))
	delta_s = math.degrees(math.asin(math.sin(math.radians(0)) * math.cos(math.radians(mean_obliquity_of_ecliptic)) + math.cos(math.radians(0)) * math.sin(math.radians(mean_obliquity_of_ecliptic)) * math.sin(math.radians(SunGeometricEclipticLongitude))))

	y_limb = math.cos(math.radians(delta_s)) * math.sin(math.radians(alpha_s - alpha_m))
	x_limb =  math.cos(math.radians(delta_m)) * math.sin(math.radians(delta_s)) - math.sin(math.radians(delta_m)) * math.cos(math.radians(delta_s)) * math.cos(math.radians(alpha_s - alpha_m))
	Moon_limb_rotation = math.degrees(math.atan( (y_limb)/(x_limb)))

	Moon_limb_rotation2 = adjust_by_quadrant(x_limb,y_limb,Moon_limb_rotation)

	print "alpha_sun:",str(alpha_s), "delta_sun",str(delta_s),"\nalpha_moon",str(alpha_m),"delta_moon",str(delta_m),"\nMoon limb rotation",str(Moon_limb_rotation2)
	
	return altitude, azimuth, altitude2, azimuth2, alpha_m2, delta_m2, age_of_moon, phase_of_moon, Moon_limb_rotation2
	#raw_input("\nPress enter to exit.")