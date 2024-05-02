import RPi.GPIO as GPIO  
from time import sleep  
GPIO.setmode(GPIO.BOARD) 

servo = 37
GPIO.setup(servo,GPIO.OUT)  
try:
    while(True):
        p = GPIO.output(servo, GPIO.HIGH)   # Sets up pin 11 as a PWM pin 
        sleep(0.01)           
        p = GPIO.output(servo, GPIO.LOW)
        sleep(0.01)
finally:
    GPIO.cleanup()           # Resets the GPIO pins back to defaults