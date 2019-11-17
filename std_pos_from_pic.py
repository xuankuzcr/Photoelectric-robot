import cv2
import numpy as np

std_pos = {}
std_pos_put = {}
for i in range(1, 5):
    try:
        file_path = "/home/pi/Desktop/std_pos/" + str(i) + ".jpg"
        print "Attempting to read image from path: %s" % file_path
        frame_origin = cv2.imread(file_path)
        gray_grab = cv2.cvtColor(frame_origin, cv2.COLOR_RGB2GRAY)
        circles = cv2.HoughCircles(gray_grab, cv2.cv.CV_HOUGH_GRADIENT, 2, 100, maxRadius=100)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            x, y, r = circles[0]
            std_pos[str(i)] = [x, y]
            print "std_pos[" + str(i) + "] x_origin: %d, y_origin: %d" % (x, y)
    except Exception as e:
        print e
for key in ["red0", "green0", "blue0", "white0", "black0", "red1", "green1", "blue1", "white1"]:
    try:
        file_path = "/home/pi/Desktop/std_pos/" + key + ".jpg"
        print "Attempting to read image from path: %s" % file_path
        frame_origin = cv2.imread(file_path)
        gray_grab = cv2.cvtColor(frame_origin, cv2.COLOR_RGB2GRAY)
        circles = cv2.HoughCircles(gray_grab, cv2.cv.CV_HOUGH_GRADIENT, 2, 100, maxRadius=100)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            x, y, r = circles[0]
            std_pos_put[key] = [x, y]
            print "std_pos_put[" + key + "] x_origin: %d, y_origin: %d" % (x, y)
        else:
            print "Cannot detect circle from standard picture: " + key
    except Exception as e:
        print e
        print "Error detecting circles from standard picture: " + key
