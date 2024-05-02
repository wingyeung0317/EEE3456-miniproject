import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
pir = 10
GPIO.setup(pir, GPIO.IN)
moved = 0
sleep(2)      #give sensor to startup

try:
    while True:
        moved = GPIO.input(pir)
        if moved == 1:
            print("Motion detected!")
                
        sleep(0.2)

finally:
    print("Exit the program...")
    GPIO.cleanup()
