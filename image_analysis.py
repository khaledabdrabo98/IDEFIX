# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(1280, 720))
# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	frame = image.array

	# Convert the frame in BGR(RGB color space) to
	# HSV(hue-saturation-value) color space
	hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# Set range for red color and define mask
	red_lower = np.array([136, 87, 111], np.uint8)
	red_upper = np.array([180, 255, 255], np.uint8)
	red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

	# Set range for green color and define mask
	green_lower = np.array([25, 52, 72], np.uint8)
	green_upper = np.array([102, 255, 255], np.uint8)
	green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

	# Morphological Transform, Dilation for each color and bitwise_and operator
	# between frame and mask determines to detect only that particular color
	kernal = np.ones((5, 5), "uint8")

	# Red color
	red_mask = cv2.dilate(red_mask, kernal)
	res_red = cv2.bitwise_and(frame, frame,
							  mask = red_mask)

	# Green color
	green_mask = cv2.dilate(green_mask, kernal)
	res_green = cv2.bitwise_and(frame, frame,
								mask = green_mask)


	# Creating contour to track red color
	contours, hierarchy = cv2.findContours(red_mask,
										   cv2.RETR_TREE,
										   cv2.CHAIN_APPROX_SIMPLE)

	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			frame = cv2.rectangle(frame, (x, y),
									   (x + w, y + h),
									   (0, 0, 255), 1)
			str_coord = "Red LED ("+str(x)+", "+str(y)+")"
			cv2.putText(frame, str_coord, (x, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5,
						(0, 0, 255))

	# Creating contour to track green color
	contours, hierarchy = cv2.findContours(green_mask,
										   cv2.RETR_TREE,
										   cv2.CHAIN_APPROX_SIMPLE)

	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			frame = cv2.rectangle(frame, (x, y),
									   (x + w, y + h),
									   (0, 255, 0), 1)
			str_coord = "Green LED ("+str(x)+", "+str(y)+")"
			cv2.putText(frame, str_coord, (x, y),
						cv2.FONT_HERSHEY_SIMPLEX,
						0.5, (0, 255, 0))

	# Show frames
	cv2.imshow("LED Color detection", frame)

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	if cv2.waitKey(10) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break

