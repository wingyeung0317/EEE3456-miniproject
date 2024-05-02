# %%
import RPi.GPIO as GPIO
import time
import dht11
import threading
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
pir = 15
GPIO.setup(pir, GPIO.IN)
moved = 0
time.sleep(2)      #give sensor to startup
dht = dht11.DHT11(pin = 2)     #GPIO.2 (i.e. physical pin 3)

# %%
def dht_data():
    while True:
        repeat.wait()
        repeat.clear()
        result = dht.read()
        if result.is_valid():
            print(time.strftime('%d/%m/%y')+" "+time.strftime('%H:%M')+"\tTemp={0:0.1f}C  Humidity={1:0.1f}%".format(result.temperature, result.humidity))

dht_thread = threading.Thread(target=dht_data)

# %%
def pir_data():
    while True:
        repeat.wait()
        repeat.clear()
        moved = GPIO.input(pir)
        if moved == 1:
            print("Motion detected!")

pir_thread = threading.Thread(target=pir_data)

# %%
repeat = threading.Event()

dht_thread.start()
pir_thread.start()

while True:
    repeat.set()