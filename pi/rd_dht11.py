import RPi.GPIO as GPIO
import time
import dht11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

dht = dht11.DHT11(pin = 2)     #GPIO.2 (i.e. physical pin 3)

while True:
    result = dht.read()

    if result.is_valid():
        print(time.strftime('%d/%m/%y')+" "+time.strftime('%H:%M')+"\tTemp={0:0.1f}C  Humidity={1:0.1f}%".format(result.temperature, result.humidity))

        #print("Temperature: %d C" % result.temperature)
        #print("Humidity: %d %%" % result.humidity)