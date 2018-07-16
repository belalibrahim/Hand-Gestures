import cv2
import numpy as np
from analyzer import *
from Algorithms.DTW import *
from Algorithms.dollar import *
from Algorithms.ndollar import *

recording = False
cam = cv2.VideoCapture(0)
dtw = DTWRecognizer()
dollar = DollarRecognizer()
ndollar = NDollarRecognizer()
x0, y0, width = 250, 50, 330
points = np.array([], np.int32)
gesture = []

while cam.isOpened():

    _, frame = cam.read()
    frame = cv2.flip(frame, 1)

    roi = get_roi(frame, x0, y0, width)
    grey, blur, threshold, contours = get_filtered_frame(roi)

    count_defects = -1
    drawing = np.zeros(roi.shape, np.uint8)

    try:
        cnt = max(contours, key=lambda x: cv2.contourArea(x))

        if recording:
            cv2.putText(frame, "Capturing", (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Press 'c' to capture a gesture", (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 0)

        hull = cv2.convexHull(cnt)

        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 1)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 1)

        hull = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull)

        if type(defects) != type(None):
            count_defects = 0
            for i in range(defects.shape[0]):
                start, end, far = get_defects_points(defects, i, cnt)
                angle = get_angle(start, end, far)

                if angle <= math.pi / 2:
                    count_defects += 1
                    cv2.line(roi, start, end, [0, 255, 0], 2)

            if recording:
                if count_defects == 0:
                    centroid = get_centroid(cnt)
                    if centroid:
                        farthest_point = get_farthest_point(defects, cnt, centroid)
                        if farthest_point:
                            gesture.append(Point(farthest_point[0], farthest_point[1]))
                            points = np.append(points, farthest_point)
                            points = points.reshape(-1, 1, 2)
                            cv2.circle(roi, farthest_point, 15, [255, 0, 0], 5)
                cv2.polylines(roi, [points], False, [0, 0, 255], 5)
            else:
                gesture = []
                points = np.array([], np.int32)
    except:
        pass

    if 0 <= count_defects <= 4:
        cv2.putText(frame, str(count_defects + 1), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
    else:
        if recording:
            recording = False
            print("Stopped")
        cv2.putText(frame, "0", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('Camera', frame)
    cv2.imshow('Contours', drawing)
    cv2.imshow('Threshold', np.hstack((threshold, blur, grey)))

    k = cv2.waitKey(10)
    if k == 27:
        break
    elif k == ord('r'):
        if recording:
            recording = False
            print(count_defects+1)
            dtw.add_template(count_defects + 1, gesture)
            print("Stopped")
        else:
            recording = True
            print("Recording")

    elif k == ord('c'):
        if recording:
            recording = False
            dtw_result = dtw.Recognize(gesture)
            dollar_result = dollar.Recognize(gesture)
            ndollar_result = ndollar.Recognize([gesture])
            print("Algorithm: DTW | Gesture: " + dtw_result.Name + ", Score: " + str(dtw_result.Score))
            print("Algorithm: 1$. | Gesture: " + dollar_result.Name + ", Score: " + str(dollar_result.Score))
            print("Algorithm: N$. | Gesture: " + ndollar_result.Name + ", Score: " + str(ndollar_result.Score))
            print("Stopped")
        else:
            recording = True
            print("Capturing")
