from src.tcpcom.tcpcom import TCPServer
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import json
import numpy as np
from time import sleep

tcp_ip = "172.20.10.3"
tcp_port = 5432
tcp_reply = "Message received!"
waiting_for_config = "Waiting for configuration..."
config_received_reply = "Configuration received!"
config_false_format_reply = "Bad configuration format, please retry"
tcp_start_sending_coord = "Sending coordinates..."

# divise par la resolution les pos finales
CAM_RES_WIDTH = 1280
CAM_RES_HEIGHT = 720
FRAME_RATE = 32


def is_json(message):
    try:
        json.loads(message)
    except ValueError as e:
        return False
    return True


class PiCam:
    def __init__(self):
        super().__init__()
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

            # Send data (red & green LED coord) to client if connected
            message = "\n"
            if receivedConfig:
                print("Server:-- Sending data...")
                if not cam.coord_red_led and not cam.coord_green_led:
                    print("\nNo LED detected!")
                    message += "No data\n"
                elif cam.coord_red_led:
                    print("\nRed LED coord: \n" + cam.coord_red_led)
                    message += "Red LED coord: \n" + cam.coord_red_led
                elif cam.coord_green_led:
                    print("\nGreen LED coord: \n" + cam.coord_green_led + "\n")
                    message += "Green LED coord: \n" + cam.coord_green_led + "\n"
                server.sendMessage(message)

            # Show frames
            cv2.imshow("LED Color detection", frame)

            # Clear the stream in preparation for the next frame
            self.raw_capture.truncate(0)

            key = cv2.waitKey(10) & 0xFF
            if (key == ord('q')) or (key == 27):
                if isConnected:
                    print("Server:-- Closing connection.")
                    server.disconnect()
                print("Server:-- Closing server.")
                cv2.destroyAllWindows()
                server.terminate()
                break


def onStateChanged(state, msg):
    global isConnected, receivedConfig, config

    if state == "LISTENING":
        isConnected = False
        receivedConfig = False
        print("Server:-- Listening...")
    elif state == "CONNECTED":
        isConnected = True
        print("Server:-- Connected to client w/ip: " + msg)
        print(waiting_for_config)
    elif state == "MESSAGE":
        if is_json(msg):
            receivedConfig = True
            config = json.loads(msg)
            server.sendMessage("CONFIG OK")
            print(config_received_reply)
            print("Config ", config)
            print(tcp_start_sending_coord)
        else:
            server.sendMessage("CONFIG NOT OK")
            print(config_false_format_reply)
            receivedConfig = False


def main():
    global server, cam
    server = TCPServer(tcp_port, stateChanged=onStateChanged)
    cam = PiCam()
    # Start getting cam feed
    cam.capture()


if __name__ == '__main__':
    main()
