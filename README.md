# Moon
Calculates and shows the position and phase of the moon.   
Inputs are date,time and observer coordinates.  
Multi-touch support and selection animations.    
Runs on Linux, Windows, OS X, Android, iOS, and Raspberry Pi. You can run the same code on all supported platforms.

The position of the moon is represented by how far left(East) or right(West) it appears in the window, a central position corresponds to the moon placed directly South of the observer. The height represents the altitude.

Demo video https://streamable.com/nt2cx

---------------------------------------------------------------------
Change to tab indent 4spaces to read comments clearly

Dependencies :
 * Kivy https://kivy.org/#download
 * DateTimePicker https://github.com/kivy-garden/garden.datetimepicker
 * leapseconds https://github.com/eggert/tz/blob/master/leap-seconds.list  
    + If on Windows or an error, at line 80 (in this file) "use_fallback"  must be set to "True" : use_fallback=True 
