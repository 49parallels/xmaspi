import sys
sys.path.append("/usr/lib/python2.7")
sys.path.append("/usr/lib/python2.7/plat-arm-linux-gnueabihf")
sys.path.append("/usr/lib/python2.7/lib-tk")
sys.path.append("/usr/lib/python2.7/lib-old")
sys.path.append("/usr/lib/python2.7/lib-dynload")
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
sys.path.append("/usr/lib/python2.7/dist-packages")
sys.path.append("/usr/lib/python2.7/dist-packages/gtk-2.0")
from yeelight import Bulb
import serial
import time
import numpy
import re
import random
import urllib2
import pygame

#['/home/pi/Yeelight', '/usr/lib/python2.7', '/usr/lib/python2.7/plat-arm-linux-gnueabihf', '/usr/lib/python2.7/lib-tk', '/usr/lib/python2.7/lib-old', '/usr/lib/python2.7/lib-dynload', '/home/pi/.local/lib/python2.7/site-packages', '/usr/local/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages/gtk-2.0']

#started = False

started = False
def avg_brightness(bulb, new_data_point, window, frequency):
  global started
  window.append(new_data_point)
  if (len(window) >= frequency):
    print(window)# Now is the only time we calculate an average
    average = numpy.mean(window)
    print(average)
    # reverseAverage = 100 - average
    
    if average < 25:
            #   playMusic()
        bulb.set_brightness(100) # Using your function to save the average
        bulb.set_rgb(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
        #toggleMusic(bulb)
    elif 25 < average < 50:
            #   playMusic()
        bulb.set_brightness(75)
        bulb.set_rgb(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
        #toggleMusic(bulb)
    elif 50 < average < 75:
            #   playMusic()
        bulb.set_brightness(50)
        bulb.set_rgb(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
        #toggleMusic(bulb)
    else:
        #bulb.stop_music()
        #time.sleep(1)
        bulb.turn_off()
        started = False
        
     #   bulb.set_rgb(0,0,0)
     #   pygame.mixer.music.pause()
     #   bulb.turn_off()
     #   started = False
    
    window = [] # Clear window to collect the next 5 seconds of data
  return window


def toggleMusic(bulb):
    global started
    if not started:
        try:
            started = True
            bulb.start_music()
        except:
            print("Already in music mode.")


is_playing = False
def playMusic():
    if pygame.mixer.music.get_busy() == False:
        pygame.mixer.music.unpause()

def main():
    print "Started..."
    time.sleep(1)
    #pygame.mixer.init()
    #pygame.mixer.music.load("/home/pi/Yeelight/tma.mp3")
    #pygame.mixer.music.set_volume(1.0)
    #pygame.mixer.music.play()
    #pygame.mixer.music.pause()


    bulb = Bulb("10.0.0.1", auto_on=True)
    bulb.turn_on()
    time.sleep(1)
    bulb.turn_off()
    #bulb.start_music(666, "10.0.0.2")
    #bulb.start_music()
    print(bulb.get_properties())
    ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate=9600

    window = []
    while True:
        percentage=ser.readline()
        sanitized = re.sub("[^0-9]", "", percentage)
        if sanitized:
            window = avg_brightness(bulb, int(sanitized), window, 5)
            time.sleep(0.200)
            #time.sleep(0.200)


def wait_for_internet_connection():
    while True:
        try:
            response = urllib2.urlopen('http://49parallels.com',timeout=1)
            return
        except urllib2.URLError:
            pass



wait_for_internet_connection()
main()
