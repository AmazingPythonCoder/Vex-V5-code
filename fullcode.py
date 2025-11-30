# This is Maxence Doing the job a second

from vex import *

brain = Brain()
controller = Controller()

leftMotor  = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
rightMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)

intake1 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
intake2 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)

intake1_speed = 50
intake2_speed = 50

drivetrain = DriveTrain(leftMotor, rightMotor, 319.19, 320, 40, MM)

DEADBAND = 5

def db(x):
    return 0 if abs(x) < DEADBAND else x

def autonomous():
    drivetrain.drive_for(FORWARD, 600, MM)
    drivetrain.turn_for(RIGHT, 90, DEGREES)
    drivetrain.drive_for(FORWARD, 400, MM)

def drivercontrol():
    while True:
        # Brake button L2
        if controller.buttonL2.pressing():
            leftMotor.stop(BRAKE)
            rightMotor.stop(BRAKE)
        else:
            forward = db(controller.axis3.position())
            turn    = db(controller.axis1.position())

            left_speed  = forward + turn
            right_speed = forward - turn

            # Slow mode with L1
            if controller.buttonL1.pressing():
                left_speed  *= 0.20
                right_speed *= 0.20

            leftMotor.spin(FORWARD, left_speed, PERCENT)
            rightMotor.spin(FORWARD, right_speed, PERCENT)
        
        # Intake controls
        if controller.buttonR1.pressing():
            intake1.spin(FORWARD, intake1_speed, PERCENT)
            intake2.spin(FORWARD, intake2_speed, PERCENT)
        elif controller.buttonR2.pressing():
            intake1.spin(REVERSE, intake1_speed, PERCENT)
            intake2.spin(REVERSE, intake2_speed, PERCENT)
        else:
            intake1.stop(COAST)
            intake2.stop(COAST)

        wait(20, MSEC)

comp = Competition(drivercontrol, autonomous)







