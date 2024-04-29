import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
led = 12
pir = 15
GPIO.setup(led, GPIO.OUT)
GPIO.setup(pir, GPIO.IN)
moved = 0
sleep(2)      #give sensor to startup

try:
    while True:
        moved = GPIO.input(pir)
        if moved == 1:
            GPIO.output(led, True)
            print("Motion detected!")
                
        else:
            GPIO.output(led, False)
        sleep(0.2)

finally:
    print("Exit the program...")
    GPIO.cleanup()
