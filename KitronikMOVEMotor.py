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

from microbit import i2c, pin3, pin12, pin15, pin16, display, sleep
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

# Servo Constants
SERVO_MIN_PULSE = 500 #microsec
SERVO_MAX_PULSE = 2500 #microsec
SERVO_DEGREE_RANGE = 180
SERVO_DEG_TO_uS = (SERVO_MAX_PULSE - SERVO_MIN_PULSE) / SERVO_DEGREE_RANGE
SERVO_PWM_PERIOD = 20 #ms

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
        
        # now setup PWM on the servo pin
        pin15.set_analog_period(SERVO_PWM_PERIOD)
        pin16.set_analog_period(SERVO_PWM_PERIOD)

    # A couple of 'raw' speed functions for the motors.
    # these functions expect speed -255 -> +255
    def LeftMotor(self, speed):
        if self.moveMotorVersion != 31:
            speed = int(speed)
            if speed > 255:
                speed = 255
            elif speed < -255:
                speed = -255
            motorForward = bytearray([0, 0])
            motorBackward = bytearray([0, 0])
            motorForward[0] = LEFT_MOTOR
            motorBackward[0] = LEFT_MOTOR + 1
            if speed > 0:
                # going forwards
                motorForward[1] = speed
            elif speed < 0: 
                # going backwards
                motorBackward[1] = speed * -1
            i2c.write(CHIP_ADDR, motorForward, False)
            i2c.write(CHIP_ADDR, motorBackward, False)

        else:
            speed = int(speed)
            if speed > 255:
                speed = 255
            elif speed < -255:
                speed = -255
            motor = bytearray([0, 0, 0])
            motorJump = bytearray([0, 0, 0])
            if speed > 0:
                # going forwards
                motor[0] = speed
                motorJump[0] = 255
            elif speed < 0: 
                # going backwards
                motor[1] = speed * -1
                motorJump[1] = 255
            else:
                # stopping
                motor[2] = 255
            self.ws2811[1] = (motorJump[0], motorJump[1], motorJump[2])
            self.ws2811.show()
            sleep(1) # 1 ms
            self.ws2811[1] = (motor[0], motor[1], motor[2])
            self.ws2811.show()

    #speed -255 -> +255
    def RightMotor(self,speed):
        if self.moveMotorVersion != 31:
            speed = int(speed)
            if speed > 255:
                speed = 255
            elif speed < -255:
                speed = -255
            motorForward = bytearray([0, 0])
            motorBackward = bytearray([0, 0])
            motorForward[0] = RIGHT_MOTOR + 1
            motorBackward[0] = RIGHT_MOTOR
            if speed > 0:
                # going forwards
                motorForward[1] = speed
            elif speed < 0: 
                # going backwards
                motorBackward[1] = speed * -1
            i2c.write(CHIP_ADDR, motorForward, False)
            i2c.write(CHIP_ADDR, motorBackward, False)

        else:
            speed = int(speed)
            if speed > 255:
                speed = 255
            elif speed < -255:
                speed = -255
            motor = bytearray([0, 0, 0])
            motorJump = bytearray([0, 0, 0])
            if speed > 0:
                # going forwards
                motor[1] = speed
                motorJump[1] = 255
            elif speed < 0: 
                # going backwards
                motor[0] = speed * -1
                motorJump[0] = 255
            else:
                # stopping
                motor[2] = 255
            self.ws2811[0] = (motorJump[0], motorJump[1], motorJump[2])
            self.ws2811.show()
            sleep(1) # 1 ms
            self.ws2811[0] = (motor[0], motor[1], motor[2])
            self.ws2811.show()

    # A function that stops both motors, rather than having to call Left and Right with zero speed.
    def StopMotors(self):
        if self.moveMotorVersion != 31:
            stopBuffer = bytearray([0, 0])
            stopBuffer[0] = LEFT_MOTOR
            i2c.write(CHIP_ADDR, stopBuffer, False)
            stopBuffer[0] = LEFT_MOTOR + 1
            i2c.write(CHIP_ADDR, stopBuffer, False)
            stopBuffer[0] = RIGHT_MOTOR
            i2c.write(CHIP_ADDR, stopBuffer, False)
            stopBuffer[0] = RIGHT_MOTOR + 1
            i2c.write(CHIP_ADDR, stopBuffer, False)
        else:
            self.ws2811[0] = (0, 0, 255)
            self.ws2811[1] = (0, 0, 255)
            self.ws2811.show()
    
    # Servo Control
    # servo is expected to be 1 or 2, as per the silk on the buggy.
    # Servos are on Pins 15 and 16. We write an analog to them.
    # goToPosition converts degrees to microseconds and calls gotoPeriod, 
    def goToPosition(self, servo, degrees):
        period = SERVO_MIN_PULSE + (SERVO_DEG_TO_uS * degrees)
        self.goToPeriod(servo, period)
        
    def goToPeriod(self, servo, period):
        if servo < 1:
            servo = 1
        elif servo > 2:
            servo = 2
        if period < SERVO_MIN_PULSE:
            period = SERVO_MIN_PULSE
        elif period > SERVO_MAX_PULSE:
            period = SERVO_MAX_PULSE
        duty = round(period * 1024 * 50 // 1000000) #1024-steps in analog, 50Hz frequency, // to convert to uS
        if servo == 1:
            pin15.write_analog(duty)
        elif  servo == 2:
            pin16.write_analog(duty)
