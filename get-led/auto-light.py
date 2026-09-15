import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
delNapr = 6
GPIO.setup(delNapr, GPIO.IN)
