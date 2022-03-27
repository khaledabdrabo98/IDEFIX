from src.tcpcom.tcpcom import TCPServer
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
from threading import Thread
import numpy as np
from time import sleep

tcp_ip = "192.168.1.151"
tcp_port = 5432
tcp_reply = "Message received!"

CAM_RES_WIDTH = 1280
CAM_RES_HEIGHT = 720
FRAME_RATE = 32


def change_brightness(image, value=30):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] = v[v <= lim] + value

    final_hsv = cv2.merge((h, s, v))
    final_frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return final_frame


class PiCam:
    def __init__(self):
        super().__init__()
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = (CAM_RES_WIDTH, CAM_RES_HEIGHT)
        self.camera.framerate = FRAME_RATE
        self.raw_capture = PiRGBArray(self.camera, size=(CAM_RES_WIDTH, CAM_RES_HEIGHT))
        self.coord_red_led = ""
        self.coord_green_led = ""
        # allow the camera to warmup
        sleep(0.1)

    def capture(self):
        # capture frames from the camera
        for image in self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True):
            self.coord_red_led = ""
            self.coord_green_led = ""

            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            frame = image.array

            # decrease frame brightness
            frame = change_brightness(frame, -30)

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
                if (area > 300):
                    x, y, w, h = cv2.boundingRect(contour)
                    frame = cv2.rectangle(frame, (x, y),
                                          (x + w, y + h),
                                          (0, 0, 255), 1)
                    str_coord = "Red LED (" + str(x) + ", " + str(y) + ")"
                    self.coord_red_led += "[(" + str(x) + ", " + str(y) + "), (" + str(x + w) + ", " + str(
                        y + h) + ")]\n"
                    cv2.putText(frame, str_coord, (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 0, 255))

            # Creating contour to track green color
            contours, hierarchy = cv2.findContours(green_mask,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)

            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if (area > 300):
                    x, y, w, h = cv2.boundingRect(contour)
                    frame = cv2.rectangle(frame, (x, y),
                                          (x + w, y + h),
                                          (0, 255, 0), 1)
                    str_coord = "Green LED (" + str(x) + ", " + str(y) + ")"
                    self.coord_green_led += "[(" + str(x) + ", " + str(y) + "), (" + str(x + w) + ", " + str(
                        y + h) + ")]\n"
                    cv2.putText(frame, str_coord, (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0))

            if isConnected:
                print("Server:-- Sending Red LED coord: \n" + cam.coord_red_led +
                      "\nGreen LED coord: \n" + cam.coord_green_led + "\n")
                server.sendMessage("Red LED coord: \n" + cam.coord_red_led +
                                   "\nGreen LED coord: " + cam.coord_green_led + "\n")

            # Show frames
            cv2.imshow("LED Color detection", frame)

            # clear the stream in preparation for the next frame
            self.raw_capture.truncate(0)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


def onStateChanged(state, msg):
    global isConnected

    if state == "LISTENING":
        isConnected = False
        print("Server:-- Listening...")
    elif state == "CONNECTED":
        isConnected = True
        print("Server:-- Connected to " + msg)
        server.sendMessage("Hello, client!")
    elif state == "MESSAGE":
        print("Server:-- Message received: ", msg)
        server.sendMessage(tcp_reply)


def main():
    global server, cam
    server = TCPServer(tcp_port, stateChanged=onStateChanged)
    cam = PiCam()
    thread = Thread(target=cam.capture())
    thread.start()
    thread.join()


if __name__ == '__main__':
    main()
