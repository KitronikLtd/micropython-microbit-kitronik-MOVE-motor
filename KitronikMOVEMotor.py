# microbit-module: KitronikMOVEMotor@1.1.0
# Copyright (c) Kitronik Ltd 2022. 
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

from microbit import i2c, pin3, pin12, display, sleep
import math
from neopixel import NeoPixel

# A module to simplify the driving o the motors on Kitronik :MOVE Motor buggy with micro:bit
#Some useful constants
CHIP_ADDR = 0x62 # CHIP_ADDR is the standard chip address for the PCA9632, datasheet refers to LED control but chip is used for PWM to motor driver
MODE_1_REG_ADDR = 0x00
MODE_2_REG_ADDR = 0x01
MOTOR_OUT_ADDR = 0x08 #MOTOR output register address
MODE_1_REG_VALUE = 0x00 #setup to normal mode and not to respond to sub address
MODE_2_REG_VALUE = 0x04  #Setup to make changes on ACK, outputs set to open-drain
MOTOR_OUT_VALUE = 0xAA  #Outputs set to be controled PWM registers
#Register offsets for the motors
LEFT_MOTOR = 0x04
RIGHT_MOTOR = 0x02

class MOVEMotor:

    #An initialisation function to setup the PCA chip correctly
    #Note that if the :MOVE motor is off the microPython will likely throw OS error 19 - which menas it cant talk to the I2C chip
    def __init__(self):
        self.moveMotorVersion = 0
        display.clear()
        display.off()
        pin3.write_digital(1)
        sleep(100)
        if pin12.read_digital() == 1:
            pin3.write_digital(0)
            sleep(100)
            if pin12.read_digital() == 0:
                self.moveMotorVersion = 20
        
        display.on()
        buffer = bytearray(2)

        if self.moveMotorVersion == 0:
            try:
                buffer[0] = MODE_1_REG_ADDR
                buffer[1] = MODE_1_REG_VALUE
                i2c.write(CHIP_ADDR,buffer,False)
                readBuffer = i2c.read(CHIP_ADDR,1,False)
                if readBuffer[0] == MODE_1_REG_VALUE:
                    self.moveMotorVersion = 10
            except OSError:
                self.moveMotorVersion = 31
                self.ws2811 = NeoPixel(pin12, 2)
                # self.ws2811[0] = (0, 255, 255)
                # self.ws2811[1] = (255, 0, 255)
                # self.ws2811.show()
        
        if self.moveMotorVersion != 31:
            try:
                buffer[0] = MODE_1_REG_ADDR
                buffer[1] = MODE_1_REG_VALUE
                i2c.write(CHIP_ADDR,buffer,False)
                buffer[0] = MODE_2_REG_ADDR
                buffer[1] = MODE_2_REG_VALUE
                i2c.write(CHIP_ADDR,buffer,False)
                buffer[0] = MOTOR_OUT_ADDR
                buffer[1] = MOTOR_OUT_VALUE
                i2c.write(CHIP_ADDR,buffer,False)
            except OSError:
                raise OSError("Check the Micro:bit is turned on!")

    #A couple of 'raw' speed functions for the motors.
    # these functions expect speed -255 -> +255
    def LeftMotor(self,speed):
        if self.moveMotorVersion != 31:
            motorBuffer=bytearray(2)
            gndPinBuffer=bytearray(2)
            if(math.fabs(speed) > 255):
                motorBuffer[1] = 255
            elif(math.fabs(speed) < -255):
                motorBuffer[1] = -255
            else:
                motorBuffer[1] = int(math.fabs(speed))
            gndPinBuffer[1] = 0x00
            if(speed > 0):
                #going forwards
                motorBuffer[0] = LEFT_MOTOR
                gndPinBuffer[0] =LEFT_MOTOR +1
            else: #going backwards, or stopping
                motorBuffer[0] =LEFT_MOTOR +1
                gndPinBuffer[0] = LEFT_MOTOR
            i2c.write(CHIP_ADDR,motorBuffer,False)
            i2c.write(CHIP_ADDR,gndPinBuffer,False)

        else:
            speed = int(speed)
            if(speed > 255):
                speed = 255
            elif(speed < -255):
                speed = -255
            m = bytearray(3)
            mJ = bytearray(3)
            if(speed > 0):
                #going forwards
                m[0] = speed
                m[1] = 0
                mJ[0] = 255
                mJ[1] = 0
            else: 
                #going backwards, or stopping
                m[0] = 0
                m[1] = speed * -1
                mJ[0] = 0
                mJ[1] = 255
            if speed == 0:
                m[2] = 255
            else:
                m[2] = 0
                self.ws2811[1] = (mJ[0], mJ[1], mJ[2])
                self.ws2811.show()
                sleep(1)
            self.ws2811[1] = (m[0], m[1], m[2])
            self.ws2811.show()

    #speed -255 -> +255
    def RightMotor(self,speed):
        if self.moveMotorVersion != 31:
            motorBuffer=bytearray(2)
            gndPinBuffer=bytearray(2)

            if(math.fabs(speed)>255):
                motorBuffer[1] = 255
            elif(math.fabs(speed) < -255):
                motorBuffer[1] = -255
            else:
                motorBuffer[1] = int(math.fabs(speed))
            gndPinBuffer[1] = 0x00

            if(speed >0):
                #going forwards
                motorBuffer[0] =RIGHT_MOTOR +1
                gndPinBuffer[0] = RIGHT_MOTOR
            else: #going backwards
                motorBuffer[0] = RIGHT_MOTOR
                gndPinBuffer[0] =RIGHT_MOTOR +1

            i2c.write(CHIP_ADDR,motorBuffer,False)
            i2c.write(CHIP_ADDR,gndPinBuffer,False)

        else:
            speed = int(speed)
            if(speed > 255):
                speed = 255
            elif(speed < -255):
                speed = -255
            m = bytearray(3)
            mJ = bytearray(3)
            if(speed > 0):
                #going forwards
                m[0] = 0
                m[1] = speed
                mJ[0] = 0
                mJ[1] = 255
            else: 
                #going backwards, or stopping
                m[0] = speed * -1
                m[1] = 0
                mJ[0] = 255
                mJ[1] = 0
            if speed == 0:
                m[2] = 255
            else:
                m[2] = 0
                self.ws2811[0] = (mJ[0], mJ[1], mJ[2])
                self.ws2811.show()
                sleep(1)
            self.ws2811[0] = (m[0], m[1], m[2])
            self.ws2811.show()

    #A function that stops both motors, rather than having to call Left and Right with zero speed.
    def StopMotors(self):
        if self.moveMotorVersion != 31:
            stopBuffer=bytearray(2)
            stopBuffer[0] = LEFT_MOTOR
            stopBuffer[1] = 0x00
            i2c.write(CHIP_ADDR,stopBuffer,False)
            stopBuffer[0] =LEFT_MOTOR +1
            i2c.write(CHIP_ADDR,stopBuffer,False)
            stopBuffer[0] =RIGHT_MOTOR
            i2c.write(CHIP_ADDR,stopBuffer,False)
            stopBuffer[0] =RIGHT_MOTOR +1
            i2c.write(CHIP_ADDR,stopBuffer,False)

        else:
            self.ws2811[0] = (0, 0, 255)
            self.ws2811[1] = (0, 0, 255)
            self.ws2811.show()
