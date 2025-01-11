import os
import cv2 as cv
import numpy as np
import pandas as pd
import mediapipe as mp
import time
import pickle
import math
# import tensorflow


class_data = ['Full Lunge', 'Half Lunge', 'Standing']

VIDEO_SOURCE = './Dataset/stretching-exercise.mp4'
# VIDEO_SOURCE = 'rtsp://192.168.1.10:554/live.sdp'
# VIDEO_SOURCE = 0
MODEL_PATH =  './model/final_svm.pkl'
SCALER_PATH =  './model/scaler.pkl'

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


try:
    with open(MODEL_PATH, 'rb') as file:
        svm_model = pickle.load(file)
        print("Model Loaded!")
except Exception as e:
    print(f"Error loading model: {e}")


try:
    with open(SCALER_PATH, 'rb') as file:
        scaler = pickle.load(file)
        print("Model Loaded!")
except Exception as e:
    print(f"Error loading model: {e}")

def calculate_angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    rad = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])

    if rad > np.pi:
        rad -= 2 * np.pi
    elif rad < -np.pi:
        rad += 2 * np.pi

    if rad < 0:
        rad = -rad

    return rad


if __name__ == '__main__':
    result = 5
    # if VIDEO_SOURCE == 0 or VIDEO_SOURCE == '0':
    cap = cv.VideoCapture(VIDEO_SOURCE)
    print("Opening video...")

    if not cap.isOpened():
        print("Error Loading Video")
        exit(0)
    
    print(f"Video Width : {cap.get(cv.CAP_PROP_FRAME_WIDTH)}")
    print(f"Video Height : {cap.get(cv.CAP_PROP_FRAME_HEIGHT)}")
    video_fps = cap.get(cv.CAP_PROP_FPS)
    print(f"Frame Per Second : {video_fps}")

    delay = int(1.0 / video_fps * 1000)
    
    prev_time = time.time()

    with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:

        while cap.isOpened():
            ret, img= cap.read()
            rgb_img = cv.cvtColor(img,cv.COLOR_BGR2RGB)

            if not ret:
                print("Error taking the frame")
                break


            res = pose.process(rgb_img)
            # mp_drawing.draw_landmarks(img,res.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            try: 
                csv_data = []

                dict = {}
                landmarks = res.pose_landmarks.landmark
                x_nose = landmarks[0].x
                y_nose= landmarks[0].y
                z_nose= landmarks[0].z
                for i in range(23,29):
                    x = landmarks[i].x - x_nose
                    y = landmarks[i].y - y_nose
                    z = landmarks[i].z - z_nose
                    
                    x_col_name = "X"+str(i)
                    y_col_name = "Y"+str(i)
                    z_col_name = "Z"+str(i)

                    dict[x_col_name] = x
                    dict[y_col_name] = y
                    dict[z_col_name] = z
                dict['rad1'] = calculate_angle([landmarks[23].x,landmarks[23].y],[landmarks[25].x,landmarks[25].y],[landmarks[27].x,landmarks[27].y])
                dict['rad2'] = calculate_angle([landmarks[24].x,landmarks[24].y],[landmarks[26].x,landmarks[26].y],[landmarks[28].x,landmarks[28].y])
                csv_data.append(dict)
                csv_data = pd.DataFrame(csv_data)
                csv_data = scaler.transform(csv_data)
                # print(csv_data)

                result = svm_model.predict(pd.DataFrame(csv_data))
                text = f"{class_data[result[0]]}"
                (text_width, _), baseline = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 2)
                x_coordinate = int(landmarks[0].x * img.shape[1]) - text_width // 2
                y_coordinate = int(landmarks[0].y * img.shape[0])
                cv.putText(img, text, (x_coordinate, y_coordinate-50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 120), 2)



            except:
                pass

            curr_time = time.time()
            elapsed_time = curr_time - prev_time


            prev_time = curr_time
            current_fps = 1.0 / elapsed_time if elapsed_time > 0 else 1

            skipped_frames = math.ceil(elapsed_time*1000 / delay) + 1
            # print(delay/skipped_frames)
            

            # print(delay)

            cv.putText(img, f"FPS: {current_fps:.2f}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.imshow('Video', img)


            if cv.waitKey(int(delay / skipped_frames)+1) == ord('q'):
                break

    cap.release()
        
