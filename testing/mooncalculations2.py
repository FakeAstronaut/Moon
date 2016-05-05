# coding: utf-8

#Functions used for calculating the position of the moon

import calendar
import math
import datetime
import turtle
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
##########
def calculate_moon_position1(day,month,year,timeH,timeM,timeS):
	print "Calculated with set date: "+str(day)+"/"+str(month)+"/"+str(year)+"/ at " + str(timeH)+":"+str(timeM)+":"+str(timeS)+".\n"

	time_as_frac_of_day = ((timeS/60.0 + timeM)/60.0 + timeH)/24.0
	daystotal=0
	for monthdays in daysinmonth[:month-1]:
		daystotal += monthdays
	daystotal += day
	total_days = (year-1990)*365 + calendar.leapdays(1990, year+1) + daystotal + time_as_frac_of_day
	
	Mean_anomaly1 = (360/days_for_360 * total_days)
	Mean_anomaly1 = adjustrange1(Mean_anomaly1)
	Mean_anomaly2 = Mean_anomaly1 + Ecliptic_longitude - Ecliptic_longitude_of_perigee
	if Mean_anomaly2 < 0:
		Mean_anomaly2 += 360
	E_c = (360.0/pi)* eccentricity_of_orbit * math.sin(math.radians(Mean_anomaly2))
	
	SunGeometricEclipticLongitude = Mean_anomaly1 + E_c + Ecliptic_longitude
	SunGeometricEclipticLongitude = adjustrange1(SunGeometricEclipticLongitude)
	
	l  = 13.1763966 * total_days + mean_longitude
	l = adjustrange1(l)
	
	M_m = l - 0.1114041 * total_days - mean_longitude_of_perigee
	M_m = adjustrange1(M_m)
	
	N = mean_longitude_of_node - 0.0529539 * total_days	
	N = adjustrange1(N)
	
	C 	= l - SunGeometricEclipticLongitude
	E_v = 1.2739 * math.sin(math.radians(2*C - M_m))	
	
	A_e = 0.1858 * math.sin(math.radians(Mean_anomaly2))
	A_3	= 0.37   * math.sin(math.radians(Mean_anomaly2))	
	
	Corrected_anomaly = M_m + E_v - A_e - A_3			#M'_m
	
	E_c = 6.2886 * math.sin(math.radians(Corrected_anomaly))
	A_4 = 0.214 * math.sin(math.radians(2 * Corrected_anomaly))
	
	l_prime = l + E_v + E_c - A_e + A_4
	V = 0.6583 * math.sin(math.radians(2*(l_prime - SunGeometricEclipticLongitude)))
	true_longitude = l_prime + V		#l''= l' + V
	N_prime = N - 0.16 * math.sin(math.radians(Mean_anomaly2))
	y = math.sin(math.radians(true_longitude - N_prime)) * math.cos(math.radians(inclination_of_moon_orbit))
	x = math.cos(math.radians(true_longitude - N_prime))
	
	tan_yx = math.degrees(math.atan(y/x))
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

	lambda_m = tan_yx + N_prime
	beta_m = math.degrees(math.asin(math.sin(math.radians(true_longitude - N_prime)) * math.sin(math.radians(inclination_of_moon_orbit))))

	if (month == 1) or (month == 2):
		year2 = year -1
		month2 = month +12
	else:
		year2 = year
		month2= month

	if datetime.datetime(year,month,day) >= datetime.datetime(1582,10,15):
		A = int(year2/100)
		B = 2 - A + int(A/4)
	else:
		B = 0

	if year2 > 0:
		C = int(365.25 * year2)
	else:
		C = int((365.25 * year2) - 0.75)
	D = int(30.6001 * (month2 +1))
	JD = B + C + D + day + 1720994.5 ##julian days
	JD -= 2451545
	T = JD/36525.0
	change_in_mean_obliquity_of_ecliptic = 46.815 * T + 0.0006*T*T - 0.00181*T*T*T
	change_in_mean_obliquity_of_ecliptic /= 3600.0 
	mean_obliquity_of_ecliptic = 23.439292 - change_in_mean_obliquity_of_ecliptic
	alpha_m = math.degrees(math.atan((math.sin(math.radians(lambda_m)) * math.cos(math.radians(mean_obliquity_of_ecliptic)) - math.tan(math.radians(beta_m)) * math.sin(math.radians(mean_obliquity_of_ecliptic)))/math.cos(math.radians(lambda_m))))
	alpha_m = adjustrange1(alpha_m)/15.0
	alpha_m2 = decdeg2dms(alpha_m)
	
	delta_m = math.degrees(math.asin(math.sin(math.radians(beta_m)) * math.cos(math.radians(mean_obliquity_of_ecliptic)) + math.cos(math.radians(beta_m)) * math.sin(math.radians(mean_obliquity_of_ecliptic)) * math.sin(math.radians(lambda_m))))
	delta_m2 = decdeg2dms(delta_m)
	
	return T,true_longitude,SunGeometricEclipticLongitude,alpha_m,alpha_m2,delta_m,delta_m2
	
def calculate_moon_position2(T,timeH,timeM,timeS,observer_latitude,observer_longitude,alpha_m,delta_m):	
	T0 = 6.697374558 + (2400.051336 * T) + (0.000025862 * T * T)
	T0 = adjustrange2(T0)
	UT = (timeS/60.0 + timeM)/60.0 + timeH
	UT *= 1.002737909
	GST = adjustrange2(UT + T0)
	observer_longitude2 = observer_longitude/15.0

	LST = GST + observer_longitude2
	if LST > 24:
		LST -=24
	elif LST < 0:
		LST += 24

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
	azimuth2 = decdeg2dms(azimuth)
	
	return azimuth,azimuth2,altitude,altitude2
	
def calculate_moon_phase(true_longitude,SunGeometricEclipticLongitude):
	age_of_moon = true_longitude - SunGeometricEclipticLongitude
	phase_of_moon = 0.5 * (1 - math.cos(math.radians(age_of_moon)))

	return age_of_moon,phase_of_moon
