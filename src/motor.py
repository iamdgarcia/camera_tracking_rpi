import RPi.GPIO as GPIO
import time
from log import logger
class MotorInterface:
    """
    A class for controlling a servo motor using the Raspberry Pi GPIO library.

    Attributes:
        servo_pin (int): The GPIO pin connected to the servo motor.
        frequency (int): The PWM frequency for the servo motor (default is 100 Hz).
        current_pos (float): The current angle of the servo motor (default is 45 degrees).

    Methods:
        __init__(self, servo_pin: int, frequency: int = 100)
            Initializes the MotorInterface with the specified GPIO pin and frequency.

        angle_to_duty(self, ang: float) -> float
            Converts an angle in degrees to PWM duty cycle.

        goTo(self, angle: float)
            Moves the servo motor to the specified angle.

        cleanup(self)
            Cleans up the GPIO resources when done using the motor.
    """

    def __init__(self, servo_pin: int, frequency: int = 100):
        """
        Initializes the MotorInterface with the specified GPIO pin and frequency.

        Args:
            servo_pin (int): The GPIO pin connected to the servo motor.
            frequency (int, optional): The PWM frequency for the servo motor (default is 100 Hz).
        """
        self.servo_pin = servo_pin
        self.frequency = frequency

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servo_pin, self.frequency)
        logger.info(f"Initializing motor on pin {servo_pin}")

    def angle_to_duty(self, ang: float) -> float:
        """
        Converts an angle in degrees to PWM duty cycle.

        Args:
            ang (float): The angle in degrees.

        Returns:
            float: The PWM duty cycle corresponding to the angle.
        """
        return float(ang) / 10.0 + 5.0

    def goTo(self, angle: float):
        """
        Moves the servo motor to the specified angle.

        Args:
            angle (float): The target angle in degrees.
        """
        self.current_pos = angle
        duty = self.angle_to_duty(angle)
        self.pwm.ChangeDutyCycle(duty)

    def cleanup(self):
        """Cleans up the GPIO resources when done using the motor."""
        logger.info("Cleaning PWM pins")
        GPIO.cleanup()

if __name__ == '__main__':
    motor = MotorInterface(servo_pin=12, frequency=100)
