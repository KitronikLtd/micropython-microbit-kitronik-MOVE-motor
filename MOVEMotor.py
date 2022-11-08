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

from microbit import sleep
from KitronikMOVEMotor import *

# Setup buggy
buggy = MOVEMotor()
buggy.setLEDs((125, 125, 125))
buggy.showLEDs()

# Drive around in a semi random manner
while True:
    buggy.goToPosition(1, 10)
    buggy.goToPosition(2, 10)
    buggy.motorOn("l", "f", 255)
    sleep(500)
    buggy.motorOn("r", "f", 255)
    sleep(500)
    buggy.motorOff("l")
    sleep(500)
    buggy.goToPosition(1, 90)
    buggy.goToPosition(2, 90)
    buggy.motorOff("r")
    sleep(500)
    buggy.motorOn("r", "r", 255)
    sleep(500)
    buggy.motorOn("l", "r", 255)
    sleep(500)
    buggy.motorOff("r")
    sleep(500)
    buggy.goToPosition(1, 180)
    buggy.goToPosition(2, 180)
    buggy.motorOff("l")
    sleep(1000)
