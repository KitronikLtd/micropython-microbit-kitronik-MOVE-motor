# microbit-module: KitronikMOVEMotor@1.0.0
# Copyright (c) Kitronik Ltd 2019. 
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

from microbit import i2c, sleep, display, pin3, pin12
import math
import neopixel

# A module to simplify the driving o the motors on Kitronik :MOVE Motor buggy with micro:bit
# Constants for PCA9632 Driver IC
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
        # Work out which version of :MOVE Motor is in use - two different ICs for driving the motors
        try:
            i2c.read(CHIP_ADDR, 1)
        except OSError:
            self.moveMotorVersion = 31 # Version 3.1 (WS2811 driver ICs)
        else:
            display.off()
            pin3.write_digital(1)
            sleep(0.1)
            if (pin12.read_digital() == 1):
                pin3.write_digital(1)
                sleep(0.1)
                if (pin12.read_digital() == 0):
                    self.moveMotorVersion = 12 # Versions 1 and 2 (both have PCA9632 driver IC)
            display.on()
        
        # Setup the PCA9632 IC if NOT version 3.1
        if (self.moveMotorVersion == 31):
            # The motor driver uses the WS2811 ICs as a PWM driver - to access the bit-banging protocol in MicroPython, the motors have to be setup like NeiPixels
            self.motors = neopixel.NeoPixel(pin12, 2)
            self.prevLeft = (0, 0, 0)
            self.prevRight = (0, 0, 0)
        else:
            buffer = bytearray(2)
            buffer[0] = MODE_1_REG_ADDR
            buffer[1] = MODE_1_REG_VALUE
            i2c.write(CHIP_ADDR,buffer,False)
            buffer[0] = MODE_2_REG_ADDR
            buffer[1] = MODE_2_REG_VALUE
            i2c.write(CHIP_ADDR,buffer,False)
            buffer[0] = MOTOR_OUT_ADDR
            buffer[1] = MOTOR_OUT_VALUE
            i2c.write(CHIP_ADDR,buffer,False)

    # Turn off the brake lights without affecting current motor settings
    def BrakeLightsOff(self):
        self.motors[0] = (self.prevRight[0], self.prevRight[0], 0)
        self.motors[1] = (self.prevLeft[0], self.prevLeft[0], 0)
        self.motors.show()

    #A couple of 'raw' speed functions for the motors.
    # these functions expect speed -255 -> +255
    def LeftMotor(self,speed):
        if (self.moveMotorVersion == 31):
            # Limit speed value between -255 and 255
            if (speed > 255):
                speed = 255
            elif (speed < -255):
                speed = -255
            # Set speeds in correct buffer positions for forward and reverse
            if (speed > 0):
                op2 = 0
                op1 = speed
            else:
                op2 = int(math.fabs(speed))
                op1 = 0
            # If the speed is 0 (i.e. motor stopping), turn on the brake light
            if (speed == 0):
                brake = 255
            else:
                brake = 0
            # Send data to the WS2811 driver IC
            self.motors[1] = (op1, op2, brake)
            self.prevLeft = (op1, op2, brake)
            self.motors.show()
        else:
            print("v12")
            motorBuffer=bytearray(2)
            gndPinBuffer=bytearray(2)

            if(math.fabs(speed)>255):
                motorBuffer[1] = 255
            else:
                motorBuffer[1] = int(math.fabs(speed))
            gndPinBuffer[1] = 0x00

            if(speed >0):
                #going forwards
                motorBuffer[0] = LEFT_MOTOR
                gndPinBuffer[0] =LEFT_MOTOR +1
            else: #going backwards, or stopping
                motorBuffer[0] =LEFT_MOTOR +1
                gndPinBuffer[0] = LEFT_MOTOR
            i2c.write(CHIP_ADDR,motorBuffer,False)
            i2c.write(CHIP_ADDR,gndPinBuffer,False)

    #speed -255 -> +255
    def RightMotor(self,speed):
        if (self.moveMotorVersion == 31):
            # Limit speed value between -255 and 255
            if (speed > 255):
                speed = 255
            elif (speed < -255):
                speed = -255
            # Set speeds in correct buffer positions for forward and reverse
            if (speed > 0):
                op2 = speed
                op1 = 0
            else:
                op2 = 0
                op1 = int(math.fabs(speed))
            # If the speed is 0 (i.e. motor stopping), turn on the brake light
            if (speed == 0):
                brake = 255
            else:
                brake = 0
            # Send data to the WS2811 driver IC
            self.motors[0] = (op1, op2, brake)
            self.prevRight = (op1, op2, brake)
            self.motors.show()
        else:
            motorBuffer=bytearray(2)
            gndPinBuffer=bytearray(2)

            if(math.fabs(speed)>255):
                motorBuffer[1] = 255
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

    #A function that stops both motors, rather than having to call Left and Right with zero speed.
    def StopMotors(self):
        if (self.moveMotorVersion == 31):
            # Turn off both motors and turn the brake lights on
            self.motors[0] = (0, 0, 255)
            self.motors[1] = (0, 0, 255)
            self.motors.show()
        else:
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
