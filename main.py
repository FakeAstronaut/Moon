# coding: utf-8

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,ObjectProperty,StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.config import Config
from kivy.garden.datetimepicker import DatetimePicker
from mooncalculations import altitude, azimuth, altitude2, azimuth2
#Config.set('graphics', 'resizable', '0')
#Config.set('graphics', 'width', '900')
#Config.set('graphics', 'height', '700')


class MoonBall(Widget):
    moon_texture = ObjectProperty(Image(source='200_s.gif'))
	
    def move(self):
		self.pos = (self.parent.width * ((azimuth-90)/180.0)), (self.parent.height * ((altitude+3)/90.0))  ##setting the position in pixels where moon will be drawn, after scaling to correct window size

class MoonAct(Widget):
    ball = ObjectProperty(None)
    label1 = StringProperty(u"Altitude: {degrees}° {minutes}\' {seconds:.2f}\'\'".format(degrees=int(altitude2[0]), minutes=str(int(altitude2[1])).zfill(2), seconds=altitude2[2]))
    label2 = StringProperty(u"Azimuth: {degrees}° {minutes}\' {seconds:.2f}\'\'".format(degrees=int(azimuth2[0]), minutes=str(int(azimuth2[1])).zfill(2), seconds=azimuth2[2]))
    #runTouchApp(DatetimePicker())
    #self.DatetimePicker.density = 0.1
    def center_ball(self):
        self.ball.center = self.center
    
    def update(self, dt):
        #self.ball.center = self.center
        self.ball.move()
        

class MoonApp(App):
    def build(self):
        act = MoonAct()
        act.center_ball()
        Clock.schedule_interval(act.update, 1.0 / 60.0)
        return act


if __name__ == '__main__':
    MoonApp().run()
