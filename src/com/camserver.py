from src.com.tcpcom.tcpcom import TCPServer
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
from time import sleep
import json
#import config

tcp_start_sending_coord = "Sending coordinates..."

# divise par la resolution les pos finales
CAM_RES_WIDTH = 1280 #config.CAM_RES_WIDTH
CAM_RES_HEIGHT = 720 #config.CAM_RES_HEIGHT
FRAME_RATE = 32 #config.FRAME_RATE


def onStateChanged(state, msg):
    global isConnected

    if state == "LISTENING":
        isConnected = False
        print("Raspberry Pi:-- Listening...")
    elif state == "CONNECTED":
        isConnected = True
        print("Raspberry Pi:-- Connected to PC w/ip: " + msg)


class RaspiCamServer:
    def __init__(self, ipaddress, port, config):
        super().__init__()
        # Initialize TCPServer to send cam coords
        self.server = TCPServer(port, stateChanged=onStateChanged)
        self.config = config
        # Initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = (CAM_RES_WIDTH, CAM_RES_HEIGHT)
        self.camera.framerate = FRAME_RATE
        self.raw_capture = PiRGBArray(self.camera, size=(CAM_RES_WIDTH, CAM_RES_HEIGHT))
        self.coord_red_led = ""
        self.coord_green_led = ""
        # allow the camera to warmup
        sleep(0.1)

    def capture(self):
        # Capture frames from the camera
        for image in self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True):
            self.coord_red_led = ""
            self.coord_green_led = ""

            # Grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            frame = image.array

            # converting image into grayscale image
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # setting threshold of gray image
            _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

            # using a findContours() function
            squares, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Convert the frame in BGR(RGB color space) to
            # HSV(hue-saturation-value) color space
            hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Set range for red color and define mask
            red_lower = np.array([160, 155, 84], np.uint8)
            red_upper = np.array([180, 255, 255], np.uint8)
            red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

            # Set range for green color and define mask
            green_lower = np.array([50, 110, 50], np.uint8)
            green_upper = np.array([100, 200, 100], np.uint8)
            green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

            # Morphological Transform, Dilation for each color and bitwise_and operator
            # between frame and mask determines to detect only that particular color
            kernal = np.ones((5, 5), "uint8")

            # Red color
            red_mask = cv2.dilate(red_mask, kernal)
            res_red = cv2.bitwise_and(frame, frame,
                                      mask=red_mask)

            # Green color
            green_mask = cv2.dilate(green_mask, kernal)
            res_green = cv2.bitwise_and(frame, frame,
                                        mask=green_mask)

            # Creating contour to track red color
            contours, hierarchy = cv2.findContours(red_mask,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)

            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if (area > 1500):
                    x, y, w, h = cv2.boundingRect(contour)
                    frame = cv2.rectangle(frame, (x, y),
                                          (x + w, y + h),
                                          (0, 0, 255), 1)
                    str_coord = "Red LED (" + str(x) + ", " + str(y) + ")"
                    self.coord_red_led += str(x) + "," + str(y) + "," + str(w) + "," + \
                                          str(h) + ";"
                    cv2.putText(frame, str_coord, (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 0, 255))

            # Creating contour to track green color
            contours, hierarchy = cv2.findContours(green_mask,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)

            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if (area > 1500):
                    x, y, w, h = cv2.boundingRect(contour)
                    frame = cv2.rectangle(frame, (x, y),
                                          (x + w, y + h),
                                          (0, 255, 0), 1)
                    str_coord = "Green LED (" + str(x) + ", " + str(y) + ")"
                    self.coord_green_led += str(x) + "," + str(y) + "," + str(w) + "," + \
                                            str(h) + ";"
                    cv2.putText(frame, str_coord, (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0))

            # Send data (red & green LED coord) to client if connected
            coord = {'red': None, 'green': None}
            if isConnected:
                print("Cam Module:--", tcp_start_sending_coord)
                if not self.coord_red_led and not self.coord_green_led:
                    print("\nNo LED detected!")
                if self.coord_red_led:
                    print("\nRed LED coord: \n" + self.coord_red_led[:-1])
                    coord['red'] = self.coord_red_led[:-1]
                if self.coord_green_led:
                    print("\nGreen LED coord: \n" + self.coord_green_led[:-1] + "\n")
                    coord['green'] = self.coord_green_led[:-1]
                self.server.sendMessage(json.dumps(coord))

            # Show frames
            cv2.imshow("LED Color detection", frame)

            # Clear the stream in preparation for the next frame
            self.raw_capture.truncate(0)

            key = cv2.waitKey(10) & 0xFF
            if (key == ord('q')) or (key == 27):
                if isConnected:
                    print("Cam Module:-- Closing connection.")
                    self.server.disconnect()
                print("Cam Module:-- Closing camera.")
                cv2.destroyAllWindows()
                self.server.terminate()
                break
