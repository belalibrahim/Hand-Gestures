import cv2
import math
import numpy as np


def get_roi(frame, x, y, width):
    cv2.rectangle(frame, (x, y), (x + width - 1, y + width - 1), (0, 255, 0), 3)
    return frame[y:y + width, x:x + width]


def get_filtered_frame(frame):
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (35, 35), 0)
    _, threshold = cv2.threshold(blur, 170, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    _, contours, _ = cv2.findContours(threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return grey, blur, threshold, contours


def get_defects_points(defects, i, cnt):
    s, e, f, d = defects[i, 0]

    return tuple(cnt[s][0]), tuple(cnt[e][0]), tuple(cnt[f][0])


def get_angle(start, end, far):
    a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
    c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
    return math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))


def get_centroid(contour):
    moments = cv2.moments(contour)
    if moments['m00'] != 0:
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
        return cx, cy
    else:
        return None


def get_farthest_point(defects, contour, centroid):
    s = defects[:, 0][:, 0]
    cx, cy = centroid

    x = np.array(contour[s][:, 0][:, 0], dtype=np.float)
    y = np.array(contour[s][:, 0][:, 1], dtype=np.float)

    xp = cv2.pow(cv2.subtract(x, cx), 2)
    yp = cv2.pow(cv2.subtract(y, cy), 2)
    dist = cv2.sqrt(cv2.add(xp, yp))

    dist_max_i = np.argmax(dist)

    if dist_max_i < len(s):
        farthest_defect = s[dist_max_i]
        farthest_point = tuple(contour[farthest_defect][0])
        return farthest_point
    else:
        return None
