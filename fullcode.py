#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration
from vex import *

brain = Brain()
controller = Controller()

leftMotor  = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
rightMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)

intake1 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
intake2 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)

intake1_speed = 50
intake2_speed = 50

drivetrain = DriveTrain(leftMotor, rightMotor, 319.19, 320, 40, MM)

DEADBAND = 5

def db(x):
    return 0 if abs(x) < DEADBAND else x

def autonomous():
    
    intake2.spin(FORWARD, intake2_speed, PERCENT)
    intake1.spin(FORWARD, intake1_speed, PERCENT)
    wait(1000, MSEC)
    intake1.stop(COAST) 

    drivetrain.drive_for(FORWARD, 1000, MM)

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
