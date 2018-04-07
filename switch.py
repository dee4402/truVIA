import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    teamAButton = GPIO.input(17)
    if teamAButton == False:
        print('Button A Pressed')
        time.sleep(0.2)
        
    teamBButton = GPIO.input(24)
    if teamBButton == False:
        print("Button B Pressed")
        time.sleep(0.2)

    