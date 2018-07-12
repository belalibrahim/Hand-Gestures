import cv2
import numpy as np
import math

cam = cv2.VideoCapture(0)

x0, y0, width = 50, 100, 300

while cam.isOpened():

    _, frame = cam.read()
    frame = cv2.flip(frame, 1)

    cv2.rectangle(frame, (x0, y0), (x0 + width - 1, y0 + width - 1), (0, 255, 0), 3)
    roi = frame[y0:y0 + width, x0:x0 + width]

    grey = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (35, 35), 0)
    _, thresh1 = cv2.threshold(blur, 170, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    _, contours, _ = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    count_defects = -1
    drawing = np.zeros(roi.shape, np.uint8)

    try:
        cnt = max(contours, key=lambda x: cv2.contourArea(x))

        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 0)

        hull = cv2.convexHull(cnt)

        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 1)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 1)

        cnt = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        hull = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull)

        if type(defects) != type(None):
            count_defects = 0
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]

                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])

                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

                if angle <= math.pi / 2:
                    count_defects += 1
                    cv2.line(roi, start, end, [0, 255, 0], 2)
    except:
        pass

    if 0 <= count_defects <= 4:
        cv2.putText(frame, str(count_defects + 1), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "0", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('Camera', frame)
    cv2.imshow('Contours', drawing)
    cv2.imshow('Threshold', np.hstack((thresh1, blur, grey)))

    k = cv2.waitKey(10)
    if k == 27:
        break
