# coding: utf-8

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,ObjectProperty,StringProperty
from kivy.uix.spinner import Spinner
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.config import Config
from kivy.garden.datetimepicker import DatetimePicker
from mooncalculations4 import calculate_all
altitude, azimuth, altitude2, azimuth2, alpha_m2, delta_m2, age_of_moon, phase_of_moon, Moon_limb_rotation2 = calculate_all()

locations={"Location":[53.3478,-6.2597],"Dublin":[53.3478,-6.2597],"London":[51.5074,-0.1278],"New York":[40.7128,-74.0059],"Tokyo":[35.6895,139.6917]}
#Config.set('graphics', 'resizable', '0')
#Config.set('graphics', 'width', '900')
#Config.set('graphics', 'height', '700')
def updatevalues(day,month,year,timeH,timeM,timeS,observer_latitude,observer_longitude):
	global altitude
	global azimuth
	global altitude2
	global azimuth2
	global alpha_m2
	global delta_m2
	global age_of_moon
	global phase_of_moon
	global Moon_limb_rotation2
	altitude, azimuth, altitude2, azimuth2, alpha_m2, delta_m2, age_of_moon, phase_of_moon, Moon_limb_rotation2 = calculate_all(day,month,year,timeH,timeM,timeS,observer_latitude,observer_longitude)


class MoonBall(Widget):
	moon_texture = Image(source='200_s.gif')
	moon_limb_rotation = NumericProperty(Moon_limb_rotation2)
	moon_darkshade = Image(source='200_s_newmoon.gif')

	
	def move(self):
		self.moon_limb_rotation = Moon_limb_rotation2
		#self.moon_darkshade = Image(source='200_s.gif')
		self.pos = (self.parent.width * ((azimuth-90)/180.0)), (self.parent.height * ((altitude+3)/90.0))  ##setting the position in pixels where moon will be drawn, after scaling to correct window size
		if phase_of_moon * 100 <= 5:
			self.moon_darkshade.source='200_s_newmoon.gif'
		elif phase_of_moon * 100 <= 40:
			self.moon_darkshade.source='200_s_crescent.gif'
		elif phase_of_moon * 100 <= 60:
			self.moon_darkshade.source='200_s_quarter.gif'
		elif phase_of_moon * 100 <= 90:
			self.moon_darkshade.source='200_s_gibbous.gif'
		else:
			self.moon_darkshade.source='200_s.gif'
		print azimuth
		
class MoonAct(Widget):
	ball = ObjectProperty(None)
	label1 = StringProperty()
	label2 = StringProperty()
	label3 = StringProperty()
	label4 = StringProperty()
	label5 = StringProperty()
	
	def center_ball(self):
		self.ball.center = self.center
	
	def update(self, dt):
		#global inputtime
		#global lat
		#global lon
		#self.ball.center = self.center
		inputtime=self.picker.get_datetime()
		#print inputtime.second
		inputlocation =  self.locspin.text
		lat = locations[inputlocation][0]
		lon = locations[inputlocation][1]
		updatevalues(inputtime.day,inputtime.month,inputtime.year,inputtime.hour,inputtime.minute,inputtime.second,lat,lon)
		self.label1 = u"Altitude: {degrees}° {minutes}\' {seconds:.2f}\'\'".format(degrees=int(altitude2[0]), minutes=str(int(altitude2[1])).zfill(2), seconds=altitude2[2])
		self.label2 = u"Azimuth: {degrees}° {minutes}\' {seconds:.2f}\'\'".format(degrees=int(azimuth2[0]), minutes=str(int(azimuth2[1])).zfill(2), seconds=azimuth2[2])
		self.label3 = u"Right Ascension: {hours}h {minutes}m {seconds:.2f}s".format(hours=int(alpha_m2[0]), minutes=str(int(alpha_m2[1])).zfill(2), seconds=alpha_m2[2])
		self.label4 = u"Declination: {degrees}° {minutes}\' {seconds:.2f}\'\'".format(degrees=int(delta_m2[0]), minutes=str(int(delta_m2[1])).zfill(2), seconds=delta_m2[2])
		self.label5 = u"Phase Illumination: {degrees:.3f}%".format(degrees=phase_of_moon * 100)
		self.ball.move()
	
		self.ball.canvas.ask_update()

class MoonApp(App):
	def build(self):
		act = MoonAct()
		act.center_ball()
		Clock.schedule_interval(act.update, 30.0 / 60.0)
		return act
		


if __name__ == '__main__':
	MoonApp().run()
