# coding: utf-8

#Functions used for calculating the position of the moon

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
	
def dayfraction_to_hms(x):
	x = abs(x)
	hours = int(x * 24)
	minutes = int(((time_as_frac_of_day * 24) - hours )* 60)
	seconds = int((((time_as_frac_of_day * 24) - hours )* 60 - minutes) * 60)
	return (hours,minutes,seconds)
##########
def calculate_moon_position1(day,month,year,timeH,timeM,timeS):
	print "Calculated with set date: "+str(day)+"/"+str(month)+"/"+str(year)+"/ at " + str(timeH)+":"+str(timeM)+":"+str(timeS)+".\n"
	
	timeS+= 32.184 + leapseconds.dTAI_UTC_from_utc(datetime.datetime(year,month,day,timeH,timeM,timeS)).seconds
	time_as_frac_of_day = ((timeS/60.0 + timeM)/60.0 + timeH)/24.0					## Step 1 - pg 144 ############## 
	daystotal=0
	for monthdays in daysinmonth[:month-1]:
		daystotal += monthdays
	daystotal += day 																############  END  ##############
	total_days = (year-1990)*365 + calendar.leapdays(1990, year+1) + \  			## Step 2 - pg 144 ##############
		+ daystotal + time_as_frac_of_day											############  END  ##############
		
	
	Mean_anomaly1 = (360/days_for_360 * total_days)									## Step 3 - pg 144 ### Step 3 = pg 88
	Mean_anomaly1 = adjustrange1(Mean_anomaly1)										#### END #####
	Mean_anomaly2 = Mean_anomaly1 + Ecliptic_longitude - \							## Step 3 - pg 144 ### Step 4 = pg 88
		Ecliptic_longitude_of_perigee 
	if Mean_anomaly2 < 0:
		Mean_anomaly2 += 360														#### END #####
	E_c = (360.0/pi)* eccentricity_of_orbit * math.sin(math.radians(Mean_anomaly2))	## Step 3 - pg 144 ### Step 5 = pg 88
																					#### END #####
	SunGeometricEclipticLongitude = Mean_anomaly1 + E_c + Ecliptic_longitude		## Step 3 - pg 144 ### Step 6 = pg 88
	SunGeometricEclipticLongitude = adjustrange1(SunGeometricEclipticLongitude)		#### END #####
	
	l  = 13.1763966 * total_days + mean_longitude									## Step 4 - pg 144 ##############
	l = adjustrange1(l)																############  END  ##############
	
	M_m = l - 0.1114041 * total_days - mean_longitude_of_perigee					## Step 5 - pg 144 ##############
	M_m = adjustrange1(M_m)															############  END  ##############
	
	N = mean_longitude_of_node - 0.0529539 * total_days								## Step 6 - pg 144 ##############
	N = adjustrange1(N)																############  END  ##############
	
	C 	= l - SunGeometricEclipticLongitude											## Step 7 - pg 144 ##############
	E_v = 1.2739 * math.sin(math.radians(2*C - M_m))								############  END  ##############
	
	A_e = 0.1858 * math.sin(math.radians(Mean_anomaly2))							## Step 8 - pg 144 ##############
	A_3	= 0.37   * math.sin(math.radians(Mean_anomaly2))							############  END  ##############
	
	Corrected_anomaly = M_m + E_v - A_e - A_3			#M'_m 						## Step 9 - pg 144 ##############
																					############  END  ##############
	E_c = 6.2886 * math.sin(math.radians(Corrected_anomaly))						## Step 10 - pg 144 ##############
	A_4 = 0.214 * math.sin(math.radians(2 * Corrected_anomaly))						## Step 11 - pg 144 ##############
																					############  END  ##############
	l_prime = l + E_v + E_c - A_e + A_4												## Step 12 - pg 144 ##############
	V = 0.6583 * math.sin(math.radians(2*(l_prime - SunGeometricEclipticLongitude)))## Step 13 - pg 144 ##############
	true_longitude = l_prime + V		#l''= l' + V								## Step 14 - pg 144 ##############
	N_prime = N - 0.16 * math.sin(math.radians(Mean_anomaly2))						## Step 15 - pg 144 ##############
	y = math.sin(math.radians(true_longitude - N_prime)) * \						## Step 16 - pg 144 ##############
		math.cos(math.radians(inclination_of_moon_orbit))							############  END  ##############
	x = math.cos(math.radians(true_longitude - N_prime))							## Step 17 - pg 144 ##############
	
	tan_yx = math.degrees(math.atan(y/x))											## Step 18 - pg 144 ##############
	if (x < 0) and (y > 0):										##	Ecliptic to equatorial coordinate conversion, pg 40
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
			tan_yx += 180*(abs(int(tan_yx/180))+1)									############  END  ##############

	lambda_m = tan_yx + N_prime														## Step 19 - pg 144 ##############
	beta_m = math.degrees(math.asin(math.sin(math.radians(true_longitude-N_prime))*\## Step 20 - pg 144 ############## 
		math.sin(math.radians(inclination_of_moon_orbit))))							############  END  ##############

	if (month == 1) or (month == 2):												## Step 21 - pg 144 #julian days # Step 1 = pg 41 # Step 2 = pg 7
		year2 = year -1
		month2 = month +12
	else:
		year2 = year
		month2= month

	if datetime.datetime(year,month,day) >= datetime.datetime(1582,10,15):			## Step 21 - pg 144 # Step 1 = pg 41 # Step 3 = pg 7
		A = int(year2/100)
		B = 2 - A + int(A/4)
	else:
		B = 0

	if year2 > 0:																	## Step 21 - pg 144 # Step 1 = pg 41 # Step 4 = pg 7
		C = int(365.25 * year2)
	else:
		C = int((365.25 * year2) - 0.75)
	D = int(30.6001 * (month2 +1))													## Step 21 - pg 144 # Step 1 = pg 41 # Step 5 = pg 7
	JD = B + C + D + day + 1720994.5 ##julian days									## Step 21 - pg 144 # Step 1 = pg 41 # Step 6 = pg 7
	JD -= 2451545																	## Step 21 - pg 144 # Step 2 = pg 41
	T = JD/36525.0																	## Step 21 - pg 144 # Step 3 = pg 41
	change_in_mean_obliquity_of_ecliptic = 46.815 * T + 0.0006*T*T - 0.00181*T*T*T	## Step 21 - pg 144 # Step 4 = pg 41
	change_in_mean_obliquity_of_ecliptic /= 3600.0 									## Step 21 - pg 144 # Step 5 = pg 41
	mean_obliquity_of_ecliptic = 23.439292 - change_in_mean_obliquity_of_ecliptic	## Step 21 - pg 144 # Step 6 = pg 41
	alpha_m = math.degrees(math.atan((math.sin(math.radians(lambda_m)) * \			## Step 21 - pg 144 # Formulas on pg 40
		math.cos(math.radians(mean_obliquity_of_ecliptic)) - \
		math.tan(math.radians(beta_m)) * \
		math.sin(math.radians(mean_obliquity_of_ecliptic)))/ \
		math.cos(math.radians(lambda_m))))
	alpha_m = adjustrange1(alpha_m)/15.0
	alpha_m2 = decdeg2dms(alpha_m)
	
	delta_m = math.degrees(math.asin(math.sin(math.radians(beta_m)) * \
		math.cos(math.radians(mean_obliquity_of_ecliptic)) + \
		math.cos(math.radians(beta_m)) * \
		math.sin(math.radians(mean_obliquity_of_ecliptic)) * \
		math.sin(math.radians(lambda_m))))
	delta_m2 = decdeg2dms(delta_m)													############  END  ##############
	
	return T,true_longitude,SunGeometricEclipticLongitude,alpha_m,alpha_m2,delta_m,delta_m2
	
def calculate_moon_position2(day,month,year,timeH,timeM,timeS,observer_latitude,observer_longitude):	
	T,true_longitude,SunGeometricEclipticLongitude,alpha_m,alpha_m2,delta_m,delta_m2 = calculate_moon_position1(day,month,year,timeH,timeM,timeS)
	T0 = 6.697374558 + (2400.051336 * T) + (0.000025862 * T * T) 					##Converting to Horizontal coordinate system # Converting UT to GST pg17
	T0 = adjustrange2(T0)
	UT = (timeS/60.0 + timeM)/60.0 + timeH
	UT *= 1.002737909
	GST = adjustrange2(UT + T0)
	observer_longitude2 = observer_longitude/15.0									#Converting GST to LST pg20

	LST = GST + observer_longitude2
	if LST > 24:
		LST -=24
	elif LST < 0:
		LST += 24

	Hour_angle = adjustrange2(LST - alpha_m)										##pg 36
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
	azimuth2 = decdeg2dms(azimuth)
	
	return azimuth,azimuth2,altitude,altitude2
	
def calculate_moon_phase(day,month,year,timeH,timeM,timeS):
	T,true_longitude,SunGeometricEclipticLongitude,alpha_m,alpha_m2,delta_m,delta_m2 = calculate_moon_position1(day,month,year,timeH,timeM,timeS)
	age_of_moon = true_longitude - SunGeometricEclipticLongitude					##Calculating phase of the moon pg147
	phase_of_moon = 0.5 * (1 - math.cos(math.radians(age_of_moon)))

	return age_of_moon,phase_of_moon
