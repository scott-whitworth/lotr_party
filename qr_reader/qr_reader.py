#QR code reader testing script
from picamera2 import Picamera2, Preview
import cv2
import time

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()

time.sleep(2)

#Set Up Detector
detector = cv2.QRCodeDetector()

print("Grabing image:...")
image = picam2.capture_array("main")
#print(image)
print("done.")

data, bbox, _ = detector.detectAndDecode(image)

print("After detectAndDecode")
print(data)
print(bbox)


time.sleep(3)

picam2.stop()
