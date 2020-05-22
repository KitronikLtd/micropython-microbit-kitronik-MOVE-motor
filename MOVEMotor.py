# Example code for the :MOVE motor buggy
# www.kitronik.co.uk/5683
# Copyright (c) Kitronik Ltd 2020. 
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from microbit import pin8 #ZIP LEDs
from microbit import pin0 #Buzzer
from neopixel import NeoPixel
from time import sleep
from music import play,stop,BA_DING

from KitronikMOVEMotor import *

#MOVEMotor.setup()
buggy = MOVEMotor()
buggyLights = NeoPixel(pin8, 4)
#Slightly Blue tint on the Headlights
buggyLights[0] = [200,200,255] 
buggyLights[1] = [200,200,255]
#Red tail lights
buggyLights[2] = [255,0,0]
buggyLights[3] = [255,0,0]
buggyLights.show()

while True:
    #drive around in a semi random manner
    play(BA_DING, pin0, True, False)
    buggy.LeftMotor(255)
    buggy.RightMotor(255)
    sleep(1000)
    buggy.StopMotors()
    sleep(100)    
    buggy.LeftMotor(-255)
    buggy.RightMotor(255)
    sleep(250)
    buggy.StopMotors()
    sleep(100)    
    buggy.LeftMotor(255)
    buggy.RightMotor(255)
    sleep(1000)
    buggy.StopMotors()
    sleep(1000)    
    buggy.LeftMotor(255)
    buggy.RightMotor(-255)
    sleep(250)
    buggy.StopMotors()
    sleep(100)    
    buggy.LeftMotor(-255)
    buggy.RightMotor(-255)
    sleep(500)