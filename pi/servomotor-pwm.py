import RPi.GPIO as GPIO
import time

servo_pin = 26

GPIO.setmode(GPIO.BCM)

GPIO.setup(servo_pin,GPIO.OUT)
# 1.0ms的脈衝寬度 -> -90°
# 1.5ms的脈衝寬度 -> 0°
# 2.0ms的脈衝寬度 -> 90°

# so for 50hz, one frequency is 20ms
# duty cycle for -90° = (1/20)*100 = 5%
# duty cycle for 0° = (1.5/20)*100 = 7.5%
# duty cycle for 90° = (2/20)*100 = 10%

servo=GPIO.PWM(26,50)# 50hz frequency

servo.start(7.5)# starting duty cycle ( it set the servo to 0 degree )


try:
    # while True:
    servo.ChangeDutyCycle(5)
    time.sleep(0.3)
    servo.ChangeDutyCycle(9.4)
    time.sleep(0.3)
    # while True:
    #     for x in range(11):
    #         p.ChangeDutyCycle(control[x])
    #         time.sleep(0.03)
    #         print(x)
    #     for x in range(9,0,-1):
    #         p.ChangeDutyCycle(control[x])
    #         time.sleep(0.03)
    #         print(x)
           
except KeyboardInterrupt:
    GPIO.cleanup()
