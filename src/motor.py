import RPi.GPIO as GPIO
import time

class MotorInterface:
    servo_pin: int
    frecuency: int
    current_pos: float = 45
    def __init__(self, servo_pin, frequency=100):
        self.servo_pin = servo_pin
        self.frequency = frequency

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servo_pin, self.frequency)

    def angle_to_duty(self, ang):
        return float(ang) / 10.0 + 5.0

    def goTo(self,angle):
        self.current_pos = angle
        duty = self.angle_to_duty(angle)
        self.pwm.ChangeDutyCycle(duty)

    def cleanup(self):
        GPIO.cleanup()
        

if __name__ == '__main__':
    motor = MotorInterface(servo_pin=12, frequency=100)