#!/usr/bin/python

import requests
import base64
import json
import RPi.GPIO as GPIO
import time
from time import sleep
from picamera import PiCamera

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = PiCamera()
cameraNo = 2

IMAGE_PATH = '/home/pi/ea7the.jpg'
SECRET_KEY = 'sk_43749267edd479bca1ef9d7b'

entryendpoint = 'https://serene-reef-97119.herokuapp.com/api/carEntry'
exitendpoint = 'https://serene-reef-97119.herokuapp.com/api/carExit'


while True:
        input_state = GPIO.input(25)
        if input_state == False:
                print('Button Pressed')
                ## Start up PiCam
                camera.start_preview()
                ## sleep for a few seconds to let camera focus/adjust to light
                time.sleep(5)
                ## Capture photo
                camera.capture('/home/pi/image.jpg')
                ## Stop the PiCam
                camera.stop_preview()
                ## Publish "photo" event to Wia. Include the photo file.
		time.sleep(0.5)		
               
		with open(IMAGE_PATH, 'rb') as image_file:
		    img_base64 = base64.b64encode(image_file.read())

		url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)  #Replace 'ind' with  your country code
		r = requests.post(url, data = img_base64)
		#returnedresults = (json.dumps(r.json()))
		returnedresults = (r.json())

		carRegistration =  returnedresults ["results"][0]["plate"]
		carReg = {'carReg': carRegistration}
		if cameraNo == 1:
    			r=requests.post(url = entryendpoint, data = carReg )

		else:
    			r=requests.post(url = exitendpoint, data = carReg)

		result = r.text
		print(result)
		print (carRegistration)

