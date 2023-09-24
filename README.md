# Ball Tracking System Setup Instructions

In this guide, we will walk you through the process of setting up a ball tracking system using an external camera and a PWM motor. Please follow these detailed instructions to ensure a smooth setup and operation of your system.

## Prerequisites

Before you begin, make sure you have the following components and software ready:

- Raspberry Pi (any model with GPIO pins)
- PWM Motor
- External Camera
- Models downloaded

## Step 1: Connecting the PWM Motor

1.1. Visit the following link to access a tutorial on how to control servo motors with a Raspberry Pi: [PWM Motor Tutorial](https://www.digikey.com/en/maker/blogs/2021/how-to-control-servo-motors-with-a-raspberry-pi)

1.2. Follow the instructions provided in the tutorial to connect your PWM motor to the Raspberry Pi. Ensure that you connect it to a PWM (Pulse Width Modulation) pin on the GPIO header. Take note of the pin you've chosen, as you'll need it in the configuration.

## Step 2: Configuration Files

2.1. Locate the configuration file (cfg file) included with your ball tracking software. This file typically contains settings for the GPIO pin, camera index, and other parameters.

2.2. Open the configuration file using a text editor, such as Nano or Vim, and set the GPIO pin to the one you connected your PWM motor to in Step 1. Save the changes.

2.3. Navigate to the directory where your tracking application is stored and locate the "run_motor" app. Open it and test the motor movements to ensure it's working correctly. Make any necessary adjustments if the motor is not responding as expected.

## Step 3: Configure Model Path and Camera Index

3.1. Still in the configuration file (cfg file), you'll typically find settings for the model path and camera index. Ensure that these settings are correctly configured for your specific setup.

- Model Path: Specify the path to the pre-trained model used for object detection. Ensure that the model file is present in the specified directory.
- Camera Index: Set the index of the external camera you are using. If you're unsure, the default index is often 0 for the primary camera.

3.2. Save the changes made to the configuration file.

## Step 4: Running the Ball Tracking System

4.1. Open a terminal on your Raspberry Pi.

4.2. Navigate to the directory containing your ball tracking application.

4.3. Execute the "run_detector" script or command to start the ball tracking system. This script will utilize the configured settings from the cfg file.

```bash
 ./run_detector.sh
```

4.4. Observe the system's behavior. It should start tracking the ball using the external camera and controlling the PWM motor based on the detected ball's position.

Congratulations! You have successfully set up a ball tracking system using an external camera and a PWM motor. You can further fine-tune the system's parameters in the configuration file to optimize its performance based on your specific requirements.