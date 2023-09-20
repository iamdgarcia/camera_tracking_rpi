import sys
import RPi.GPIO as GPIO
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from motor import MotorInterface

class MotorControlApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Motor Control")
        self.setGeometry(100, 100, 400, 200)

        self.servo_pin = 18  # Change this to your GPIO pin number
        self.motor_interface = MotorInterface(self.servo_pin)

        self.init_ui()

    def init_ui(self):
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
        angle = self.angle_slider.value()
        self.angle_label.setText(f"Angle: {angle}")
        self.motor_interface.goTo(angle)

    def closeEvent(self, event):
        self.motor_interface.cleanup()
        GPIO.cleanup()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MotorControlApp()
    window.show()
    sys.exit(app.exec_())
