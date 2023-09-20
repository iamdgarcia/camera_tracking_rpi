import cv2
import time
import numpy as np
from multiprocessing import Process
from multiprocessing import Queue
from ultralytics import YOLO

from PIL import Image
import argparse


# define the function that handles our processing thread
def process_video(model_path:str,video_source,pwm_gpio:int,show:bool=True,enable_motor:bool=False):
    if enable_motor:
        from motor import MotorInterface
    global model
    motor_pos = [0,45,90,135,180]
    motor_index = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    queuepulls = 0.0
    detections = 0
    fps = 0.0
    qfps = 0.0
    # init video
    cap = cv2.VideoCapture(video_source)
    print("[info] W, H, FPS")
    frame_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    print(frame_w)
    print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(cap.get(cv2.CAP_PROP_FPS))

    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if enable_motor:
        motor = MotorInterface(pwm_gpio)
    # initialize the input queue (frames), output queue (out),
    # and the list of actual detections returned by the child process
    inputQueue = Queue(maxsize=1)
    outputQueue = Queue(maxsize=1)
    img = None
    out = None
    model = YOLO(model_path,task="detect")

    # construct a child process *indepedent* from our main process of
    # execution
    print("[INFO] starting process...")
    p = Process(target=classify_frame, args=(img, inputQueue, outputQueue,))
    p.daemon = True
    p.start()
    time.sleep(10)
    print("[INFO] starting capture...")

    # time the frame rate....
    timer1 = time.time()
    frames = 0
    queuepulls = 0
    timer2 = 0
    t2secs = 0

    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret == True:

            if queuepulls == 1:
                timer2 = time.time()
            # Capture frame-by-frame
            # frame = frame.array
            img = Image.fromarray(frame)
            # if the input queue *is* empty, give the current frame to
            # classify
            if inputQueue.empty():
                inputQueue.put(frame)

            # if the output queue *is not* empty, grab the detections
            if not outputQueue.empty():
                out = outputQueue.get()

            if out is not None:
                ball_xC = 0
                ball_yC = 0
                # loop over the detections
                for box  in out:
                    xmin = int(box[0])
                    ymin = int(box[1])
                    xmax = int(box[2])
                    ymax = int(box[3])
                    objID = int(box[5])
                    confidence = box[4]
                    ball_xC += (xmin+xmax)/2
                    ball_yC += (ymin+ymax)/2

                    if confidence > confThreshold:
                        # bounding box
                        cv2.rectangle(frame, (xmin, ymin),
                                    (xmax, ymax), color=(0, 0, 255))
                        detections += 1  # positive detections
                if len(out)>0:
                    ball_xC /= len(out)
                    ball_yC /= len(out)
                cv2.circle(frame,(int(ball_xC),int(ball_yC)), 5, (0,0,255), -1)            
                queuepulls += 1

                if enable_motor:
                    if ball_xC<frame_w / 3:
                        print("Ball in left side")
                        if motor_index >0:
                            motor_index -=1
                        motor.goTo(motor_pos[motor_index])
                        
                    elif ball_xC > frame_w * (2/3):
                        print("ball in right side")
                        if motor_index <len(motor_pos)-1:
                            motor_index +=1
                        motor.goTo(motor.goTo(motor_pos[motor_index]))
            if show:
                # Display the resulting frame
                cv2.rectangle(frame, (0, 0),
                            (frameWidth, 20), (0, 0, 0), -1)

                cv2.rectangle(frame, (0, frameHeight-20),
                            (frameWidth, frameHeight), (0, 0, 0), -1)
                cv2.putText(frame, 'Threshold: '+str(round(confThreshold, 1)), (10, 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1, cv2.LINE_AA)

                cv2.putText(frame, 'VID FPS: '+str(fps), (frameWidth-80, 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1, cv2.LINE_AA)

                cv2.putText(frame, 'TPU FPS: '+str(qfps), (frameWidth-80, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1, cv2.LINE_AA)

                cv2.putText(frame, 'Positive detections: '+str(detections), (10, frameHeight-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1, cv2.LINE_AA)

                cv2.putText(frame, 'Elapsed time: '+str(round(t2secs, 2)), (150, frameHeight-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1, cv2.LINE_AA)

                cv2.namedWindow('Coral', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Coral', frameWidth, frameHeight)
                cv2.imshow('Coral', frame)
                cv2.waitKey(1)

            
            # FPS calculation
            frames += 1
            if frames >= 1:
                end1 = time.time()
                t1secs = end1-timer1
                fps = round(frames/t1secs, 2)
            if queuepulls > 1:
                end2 = time.time()
                t2secs = end2-timer2
                qfps = round(queuepulls/t2secs, 2)

        # Break the loop
        else:
            break

    p.join()
    # Everything done, release the vid
    cap.release()

    cv2.destroyAllWindows()

def classify_frame(img, inputQueue, outputQueue):
    global model
    global confThreshold
    while True:
        # check to see if there is a frame in our input queue
        if not inputQueue.empty():
            # grab the frame from the input queue
            img = inputQueue.get()
            objs = model.predict(img,conf=confThreshold,verbose=False)[0]
            outputQueue.put(objs.cpu().numpy().boxes.data)

import configparser

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', help='path to cfg file', default="config.cfg")
    config = configparser.ConfigParser()

    # Load the configuration file
    args = parser.parse_args()
    config.read(args.cfg)
    modelPath = config["detector"]["model_path"]
    camera_idx = config["detector"]["camera_idx"]
    confThreshold = config["detector"].getfloat("conf_threshold")
    pwm_gpio = config["motor"].getint("gpio_pin")
    show = config["general"].getboolean("show")
    enable_motor = config["motor"].getboolean('enable')
    process_video(model_path=modelPath,video_source=camera_idx,pwm_gpio=pwm_gpio,show=show,enable_motor=enable_motor)