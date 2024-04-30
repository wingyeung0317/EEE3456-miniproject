import time, RPi.GPIO as GPIO

GPIO_TRIGGER = 16      #pin16 to trigger pin of the sensor
GPIO_ECHO = 18         #pin18 to echo pin
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT) 
GPIO.setup(GPIO_ECHO, GPIO.IN)

def measure():
  GPIO.output(GPIO_TRIGGER, False)    
  time.sleep(0.5)
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()
  while GPIO.input(GPIO_ECHO) == 0:   #keep reading the time if echo pin =0
    start = time.time()
  while GPIO.input(GPIO_ECHO) == 1:   #keep reading the time if echo pin =1 
    stop = time.time()
  elapsed = stop - start                    # time different between start and arrival
  distance = elapsed * 34300       #speed of sound = 343 m/s
  distance = distance / 2
  return distance

#main program
print("Ultrasonic Measurement")
while 1:
  cm = measure()
  print("Distance : %.1f cm" % cm)
