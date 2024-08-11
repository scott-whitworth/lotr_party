#QR code reader testing script
#from picamera2 import Picamera2, Preview
import cv2
import time

import serial

serial_port = "/dev/ttyACM0"
serial_baud = 115200

#Serial Port Set Up
print("Opening Port...")
serIn = serial.Serial(serial_port,serial_baud, timeout=0.5) #TODO: Not sure what I want to do with this timeout
print("Opened port: " + serIn.name)


#picam2 = Picamera2()
#camera_config = picam2.create_preview_configuration()
#picam2.configure(camera_config)
#picam2.start_preview(Preview.QTGL)
#picam2.start()

#time.sleep(2)

#Set up camera
cap = cv2.VideoCapture(0)

#Set Up Detector
detector = cv2.QRCodeDetector()

count = 1

while True:
	#Get the image
	_, img = cap.read()
	print("Image ",count," taken!")
	count = count + 1


	data, bbox, _ = detector.detectAndDecode(img)
	print("detector stuff:")
	print(data)
	print(bbox)

	if(bbox is not None):
		for i in range(len(bbox)) :
			cv2.line(img, tuple(bbox[i][0]), tuple(bbox[ (i+1)%len(bbox)][0]), color=(255,0,255), thickness=2)
			cv2.putText(img,data,(int(bbox[0][0][0]), int(bbox[0][0][1])-10), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
		if data:
			print("data found!: ", data)

			serIn.write(str(data+"\n").encode('utf-8'))

	print("Showing image")
	cv2.imshow("code detector",img)

	if(cv2.waitKey(1) == ord("q")):
		break

cap.release()
cv2.destroyAllWindows()


#print("Grabing image:...")
#image = picam2.capture_array("main")
#print(image)
#print("done.")

#data, bbox, _ = detector.detectAndDecode(image)

#print("After detectAndDecode")
#print(data)
#print(bbox)


#time.sleep(3)

#picam2.stop()
