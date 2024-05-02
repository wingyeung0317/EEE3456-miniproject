import time, RPi.GPIO as GPIO

class Ultrasonic:
  __echo_pin = 0
  __trig_pin = 0

  def __init__(self, ECHO_PIN, TRIGGER_PIN):
    self.__echo_pin = ECHO_PIN
    self.__trig_pin = TRIGGER_PIN

  def measure(self):
    "Return distance to cm"
    GPIO.setup(self.__echo_pin, GPIO.IN)
    GPIO.setup(self.__trig_pin, GPIO.OUT) 
    GPIO.output(self.__trig_pin, False)    
    time.sleep(0.5)
    GPIO.output(self.__trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(self.__trig_pin, False)
    start = time.time()
    while GPIO.input(self.__echo_pin) == 0:   #keep reading the time if echo pin =0
      start = time.time()
    while GPIO.input(self.__echo_pin) == 1:   #keep reading the time if echo pin =1 
      stop = time.time()
    elapsed = stop - start                    # time different between start and arrival
    distance = elapsed * 34300       #speed of sound = 343 m/s
    distance_cm = distance / 2
    return distance_cm
