import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
foto = 6
GPIO.setup(foto, GPIO.IN)
while True:
    GPIO.output(led, foto)
    foto_state = GPIO.input(foto)
    GPIO.output(led, not foto_state)
    time.sleep(0.2)