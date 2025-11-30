from vex import *

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Robot configuration constants"""
    # Motor ports
    LEFT_MOTOR_PORT = Ports.PORT1
    RIGHT_MOTOR_PORT = Ports.PORT2
    INTAKE1_PORT = Ports.PORT8
    INTAKE2_PORT = Ports.PORT3
    
    # Motor settings
    GEAR_RATIO = GearSetting.RATIO_18_1
    LEFT_MOTOR_REVERSED = False
    RIGHT_MOTOR_REVERSED = True
    INTAKE1_REVERSED = False
    INTAKE2_REVERSED = True
    
    # Intake settings
    INTAKE_SPEED = 50  # Percent
    
    # Drivetrain dimensions (in millimeters)
    WHEEL_DIAMETER = 319.19
    WHEELBASE = 320
    TRACK_WIDTH = 40
    
    # Control settings
    DEADBAND = 5
    SLOW_MODE_MULTIPLIER = 0.20
    CONTROL_LOOP_DELAY = 20  # Milliseconds


# ============================================================================
# HARDWARE INITIALIZATION
# ============================================================================

class Hardware:
    """Manages all robot hardware components"""
    
    def __init__(self):
        self.brain = Brain()
        self.controller = Controller()
        
        # Initialize drive motors
        self.left_motor = Motor(
            Config.LEFT_MOTOR_PORT,
            Config.GEAR_RATIO,
            Config.LEFT_MOTOR_REVERSED
        )
        self.right_motor = Motor(
            Config.RIGHT_MOTOR_PORT,
            Config.GEAR_RATIO,
            Config.RIGHT_MOTOR_REVERSED
        )
        
        # Initialize intake motors
        self.intake1 = Motor(
            Config.INTAKE1_PORT,
            Config.GEAR_RATIO,
            Config.INTAKE1_REVERSED
        )
        self.intake2 = Motor(
            Config.INTAKE2_PORT,
            Config.GEAR_RATIO,
            Config.INTAKE2_REVERSED
        )
        
        # Initialize drivetrain
        self.drivetrain = DriveTrain(
            self.left_motor,
            self.right_motor,
            Config.WHEEL_DIAMETER,
            Config.WHEELBASE,
            Config.TRACK_WIDTH,
            MM
        )


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def apply_deadband(value):
    """Apply deadband to controller input to prevent drift"""
    return 0 if abs(value) < Config.DEADBAND else value


# ============================================================================
# DRIVETRAIN CONTROL
# ============================================================================

class DrivetrainController:
    """Handles drivetrain control logic"""
    
    def __init__(self, hardware):
        self.hardware = hardware
    
    def calculate_tank_speeds(self, forward, turn):
        """Calculate left and right motor speeds for tank drive"""
        left_speed = forward + turn
        right_speed = forward - turn
        return left_speed, right_speed
    
    def apply_slow_mode(self, left_speed, right_speed, slow_mode_active):
        """Apply slow mode multiplier if active"""
        if slow_mode_active:
            left_speed *= Config.SLOW_MODE_MULTIPLIER
            right_speed *= Config.SLOW_MODE_MULTIPLIER
        return left_speed, right_speed
    
    def brake(self):
        """Stop drivetrain with brake"""
        self.hardware.left_motor.stop(BRAKE)
        self.hardware.right_motor.stop(BRAKE)
    
    def drive(self, left_speed, right_speed):
        """Drive the robot with specified speeds"""
        self.hardware.left_motor.spin(FORWARD, left_speed, PERCENT)
        self.hardware.right_motor.spin(FORWARD, right_speed, PERCENT)
    
    def update(self):
        """Update drivetrain based on controller input"""
        controller = self.hardware.controller
        
        # Check for brake
        if controller.buttonL2.pressing():
            self.brake()
        else:
            # Get controller inputs with deadband
            forward = apply_deadband(controller.axis3.position())
            turn = apply_deadband(controller.axis1.position())
            
            # Calculate speeds
            left_speed, right_speed = self.calculate_tank_speeds(forward, turn)
            
            # Apply slow mode if L1 is pressed
            slow_mode = controller.buttonL1.pressing()
            left_speed, right_speed = self.apply_slow_mode(
                left_speed, right_speed, slow_mode
            )
            
            # Drive motors
            self.drive(left_speed, right_speed)


# ============================================================================
# INTAKE CONTROL
# ============================================================================

class IntakeController:
    """Handles intake control logic"""
    
    def __init__(self, hardware):
        self.hardware = hardware
    
    def spin_forward(self):
        """Spin intake motors forward"""
        self.hardware.intake1.spin(FORWARD, Config.INTAKE_SPEED, PERCENT)
        self.hardware.intake2.spin(FORWARD, Config.INTAKE_SPEED, PERCENT)
    
    def spin_reverse(self):
        """Spin intake motors in reverse"""
        self.hardware.intake1.spin(REVERSE, Config.INTAKE_SPEED, PERCENT)
        self.hardware.intake2.spin(REVERSE, Config.INTAKE_SPEED, PERCENT)
    
    def stop(self):
        """Stop intake motors (coast)"""
        self.hardware.intake1.stop(COAST)
        self.hardware.intake2.stop(COAST)
    
    def update(self):
        """Update intake based on controller input"""
        controller = self.hardware.controller
        
        if controller.buttonR1.pressing():
            self.spin_forward()
        elif controller.buttonR2.pressing():
            self.spin_reverse()
        else:
            self.stop()


# ============================================================================
# AUTONOMOUS ROUTINE
# ============================================================================

class AutonomousRoutine:
    """Manages autonomous routines"""
    
    def __init__(self, hardware):
        self.hardware = hardware
    
    def drive_forward(self, distance_mm):
        """Drive forward a specified distance"""
        self.hardware.drivetrain.drive_for(FORWARD, distance_mm, MM)
    
    def turn(self, direction, angle_degrees):
        """Turn in specified direction by specified angle"""
        self.hardware.drivetrain.turn_for(direction, angle_degrees, DEGREES)
    
    def run(self):
        """Execute the main autonomous routine"""
        self.drive_forward(600)
        self.turn(RIGHT, 90)
        self.drive_forward(400)


# ============================================================================
# MAIN CONTROL FUNCTIONS
# ============================================================================

def autonomous():
    """Main autonomous function called by competition"""
    hardware = Hardware()
    routine = AutonomousRoutine(hardware)
    routine.run()


def drivercontrol():
    """Main driver control function called by competition"""
    hardware = Hardware()
    drivetrain_controller = DrivetrainController(hardware)
    intake_controller = IntakeController(hardware)
    
    while True:
        drivetrain_controller.update()
        intake_controller.update()
        wait(Config.CONTROL_LOOP_DELAY, MSEC)


# ============================================================================
# COMPETITION SETUP
# ============================================================================

comp = Competition(drivercontrol, autonomous)
