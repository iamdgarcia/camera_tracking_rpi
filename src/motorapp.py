import sys
import RPi.GPIO as GPIO
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from motor import MotorInterface

class MotorControlApp(QWidget):
    """
    PyQt5 application for controlling a servo motor using a GUI.

    Attributes:
        servo_pin (int): The GPIO pin number connected to the servo motor.
        motor_interface (MotorInterface): An instance of the MotorInterface class for motor control.

    Methods:
        __init__(self, gpio_pin: int)
            Initializes the MotorControlApp with the specified GPIO pin for motor control.

        init_ui(self)
            Initializes the GUI components and layout.

        update_motor_angle(self)
            Updates the motor's angle based on the slider value.

        closeEvent(self, event)
            Handles the application close event and cleans up GPIO resources.
    """

    def __init__(self, gpio_pin: int):
        """
        Initializes the MotorControlApp with the specified GPIO pin for motor control.

        Args:
            gpio_pin (int): The GPIO pin number connected to the servo motor.
        """
        super().__init__()

        self.setWindowTitle("Motor Control")
        self.setGeometry(100, 100, 400, 200)

        self.servo_pin = gpio_pin  # Change this to your GPIO pin number
        self.motor_interface = MotorInterface(self.servo_pin)

        self.init_ui()

    def init_ui(self):
        """
        Initializes the GUI components and layout.
        """
        layout = QVBoxLayout()

        self.angle_label = QLabel("Angle: 0")
        layout.addWidget(self.angle_label)

        self.angle_slider = QSlider(Qt.Horizontal)
        self.angle_slider.setMinimum(0)
        self.angle_slider.setMaximum(180)
        self.angle_slider.setValue(90)  # Initial angle
        self.angle_slider.valueChanged.connect(self.update_motor_angle)
        layout.addWidget(self.angle_slider)

        self.setLayout(layout)

    def update_motor_angle(self):
        """
        Updates the motor's angle based on the slider value.
        """
        angle = self.angle_slider.value()
        self.angle_label.setText(f"Angle: {angle}")
        self.motor_interface.goTo(angle)

    def closeEvent(self, event):
        """
        Handles the application close event and cleans up GPIO resources.

        Args:
            event (QCloseEvent): The close event.
        """
        self.motor_interface.cleanup()
        GPIO.cleanup()
        event.accept()


import argparse
import configparser
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', help='path to cfg file', default="config.cfg")
    config = configparser.ConfigParser()
    pwm_gpio = config["motor"].getint("gpio_pin")    # Load the configuration file
    args = parser.parse_args()
    config.read(args.cfg)
    app = QApplication(sys.argv)
    window = MotorControlApp(pwm_gpio)
    window.show()
    sys.exit(app.exec_())
