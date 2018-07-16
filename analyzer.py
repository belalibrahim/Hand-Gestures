import math

import cv2


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


def centroid(contour):
    moments = cv2.moments(contour)
    if moments['m00'] != 0:
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
        return tuple(cx, cy)
    else:
        return None
