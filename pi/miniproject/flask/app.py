from flask import Flask
import pandas as pd
import dht11 as DHT
import arrow
import st7735_custom
import pandas as pd
from IPython.display import display
from IPython.display import clear_output
from time import sleep
import digitalio
import board
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from PIL import Image
import RPi.GPIO as GPIO
import base64
from threading import Thread
import ultrasonicLib

app = Flask(__name__)

if __name__=='__main__':
    app.run(threaded=True)

# DHT LCD
lcd = st7735_custom.ST7735( cs_pin = digitalio.DigitalInOut(board.CE0),
                            dc_pin = digitalio.DigitalInOut(board.D25),
                            reset_pin = digitalio.DigitalInOut(board.D24))
lcd.image()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pir_pin = 15
servo_pin = 26
dht11 = DHT.DHT11(pin = 2)
ultrasonic_sensor = ultrasonicLib.Ultrasonic(27, 22)

GPIO.setup(pir_pin, GPIO.IN)
GPIO.setup(servo_pin,GPIO.OUT)
servo_pwm=GPIO.PWM(26,50)
moved = 0
sleep(2)      #give sensor to startup
pir_results = pd.DataFrame([],columns=["motion", "time"])
pir_plot = pir_results.copy()

dht_results = pd.DataFrame([],columns=["temperature", "humidity", "time"])
dht_plot = dht_results.copy()
pir_results = pd.DataFrame([],columns=["motion", "time"])
pir_plot = pir_results.copy()
ultrasonic_results = pd.DataFrame([],columns=["distance", "time"])
ultrasonic_plot = ultrasonic_results.copy()

plotdf = pd.concat([dht_plot, pir_plot], ignore_index=True)
plotdf['count'] = plotdf.groupby(['time'])['motion'].transform('count')

@app.route('/')
def hello():
    return 'hello world'

@app.route('/dht')
def dht():
    result = dht11.read()
    while not result.is_valid():
        result = dht11.read()
        moved = GPIO.input(pir_pin)

    if result.is_valid():
        clear_output(wait=False)
        dht_results.loc[len(dht_results.index)] = [result.temperature, result.humidity, arrow.now(tz="+08:00").format()]
        
        dht_plot = dht_results.copy()
        # dht_plot.time = dht_plot.time.apply(lambda x: arrow.get(x).format('YYYY-MM-DD HH:mm'))
        dht_plot.time = dht_plot.time.apply(lambda x: arrow.get(x).format('HH:mm'))
        print(f"Temp: {dht_results.loc[len(dht_results.index)-1, 'temperature']} \n Hum: {dht_results.loc[len(dht_results.index)-1, 'humidity']}")
        # display(dht_results)
        plotdf = pd.concat([dht_plot, pir_plot], ignore_index=True)
        display(plotdf)
        plt.figure().set_figheight(7)
        sns.lineplot(x="time", y="temperature", data=dht_plot)
        sns.lineplot(x="time", y="humidity", data=dht_plot)
        plt.yticks(np.arange(0, 101, 2))
        plt.ylabel("")
        plt.legend(["temperature", "temperature range", "humidity", "humidity range"], loc="lower right")
        
        __tmpfiledht = BytesIO()
        plt.savefig(__tmpfiledht, format='png')
        __encoded = base64.b64encode(__tmpfiledht.getvalue()).decode('utf-8')
        imghtml = '<img class="pltimg" src=\'data:image/png;base64,{}\' style="height:99%;float:left;">'.format(__encoded)
        plt.close()

        # plot = plt.show()

        # lcd.custom_rectangle(color1=st7735_custom.BLACK, color2=st7735_custom.WHITE)
        # lcd.__image = Image.open(__tmpfiledht).rotate(0).resize((lcd.width, lcd.height))
        lcd.custom_img(__tmpfiledht)
        lcd.custom_text(text=f"Temp: {dht_results.loc[len(dht_results.index)-1, 'temperature']} \n Hum: {dht_results.loc[len(dht_results.index)-1, 'humidity']}", color=st7735_custom.RED)
        lcd.image()
        html = f"""
                <html>
                <head>
                    <title>DHT11</title>
                    <script>
                        setTimeout(function()\u007b
                            location.reload();
                        \u007d, 500);
                    </script>
                </head>
                <body>
                    <h1 style="position:fixed;top:0;left:0;">Temperature and Humidity</h1>
                    <div style="height:99%;display:grid; grid-template-columns:1fr 400px">
                        {imghtml}
                        <div style="height:98%;overflow:scroll;">
                            <span>Temp: {dht_results.loc[len(dht_results.index)-1, 'temperature']}</span>
                            <span>Hum: {dht_results.loc[len(dht_results.index)-1, 'humidity']}</span>
                            {dht_results.to_html()}
                        </div>
                    </div>
                </body>
                </html>
                """
    return html

@app.route('/pir')
def pir():
    moved = GPIO.input(pir_pin)
    while moved != 1:
        moved = GPIO.input(pir_pin)

    clear_output(wait=False)
    pir_results.loc[len(pir_results.index)] = [True, arrow.now(tz="+08:00").format()]
    print("Motion detected!")
    pir_plot = pir_results.copy()
    pir_plot.time = pir_plot.time.apply(lambda x: arrow.get(x).format('YYYY-MM-DD HH:mm'))
    print(f"Motion: {pir_results.loc[len(pir_results.index)-1, 'time']}")
    # display(pir_results)
    plotdf = pd.concat([dht_plot, pir_plot], ignore_index=True)
    plotdf['count'] = plotdf.groupby(['time'])['motion'].transform('count')
    plotdf.drop_duplicates(subset=['time', 'motion'], keep='last', inplace=True)
    plotdf.reset_index(drop=True, inplace=True)
    countdf = plotdf[['time', 'count']]
    display(plotdf)
    plt.figure().set_figheight(7)
    sns.lineplot(x="time", y="count", data=countdf)
    
    __tmpfilepir = BytesIO()
    plt.savefig(__tmpfilepir, format='png')
    __encoded = base64.b64encode(__tmpfilepir.getvalue()).decode('utf-8')
    imghtml = '<img class="pltimg" src=\'data:image/png;base64,{}\' style="height:99%;float:left;">'.format(__encoded)
    plt.close()

    lcd.custom_img(__tmpfilepir)
    lcd.custom_text(text=f"Last movement: \n{arrow.get(pir_results.loc[len(pir_results.index)-1, 'time']).format('YYYY-MM-DD')} \n{arrow.get(pir_results.loc[len(pir_results.index)-1, 'time']).format('HH:mm:ss')}", color=st7735_custom.RED)
    lcd.image()
    html = f"""
            <html>
            <head>
                <title>PIR</title>
                <script>
                    setTimeout(function()\u007b
                        location.href = location.href; 
                    \u007d, 1000);
                </script>
            </head>
            <body>
                <h1 style="position:fixed;top:0;left:0;">PIR</h1>
                <div style="height:99%;display:grid; grid-template-columns:1fr 280px 300px;">
                    {imghtml}
                    <div style="height:98%;overflow:scroll;">
                        {countdf.to_html()}
                    </div>
                    <div style="height:98%;overflow:scroll;">
                        {pir_results.to_html()}
                    </div>
                </div>
            </body>
            </html>
            """
    return html

@app.route("/ultrasonic")
def ultrasonic():
    clear_output(wait=False)
    ultrasonic_results.loc[len(ultrasonic_results.index)] = [ultrasonic_sensor.measure(), arrow.now(tz="+08:00").format()]
    ultrasonic_plot = ultrasonic_results.copy()
    ultrasonic_plot.time = ultrasonic_plot.time.apply(lambda x: arrow.get(x).format('mm:ss'))
    sns.scatterplot(x="time", y="distance", data=ultrasonic_plot)
    plt.ylabel("distance (cm)")
    __tmpfileultrasonic = BytesIO()
    plt.savefig(__tmpfileultrasonic, format='png')
    __encoded = base64.b64encode(__tmpfileultrasonic.getvalue()).decode('utf-8')
    imghtml = '<img class="pltimg" src=\'data:image/png;base64,{}\' style="height:99%;float:left;">'.format(__encoded)
    plt.close()
    lcd.custom_img(__tmpfileultrasonic)
    lcd.custom_text(text=f"Lastest Measurement: \n{ultrasonic_results.loc[len(ultrasonic_results.index)-1, 'distance']}", color=st7735_custom.RED)
    lcd.image()
    html = f"""
        <html>
        <head>
            <title>Ultrasonic Sensor</title>
            <script>
                setTimeout(function()\u007b
                    location.href = location.href; 
                \u007d, 200);
            </script>
        </head>
        <body>
            <h1 style="position:fixed;top:0;left:0;">Ultrasonic Sensor</h1>
            <div style="height:99%;display:grid; grid-template-columns:1fr 280px;">
                {imghtml}
                <div style="height:98%;overflow:scroll;">
                    {ultrasonic_results.to_html()}
                </div>
            </div>
        </body>
        </html>
        """
    return html

@app.route("/servo")
def servo():
    clear_output(wait=False)
    lcd.custom_rectangle(st7735_custom.BLACK, st7735_custom.BLACK)
    lcd.image()
    servo_pwm.start(7.25)
    html = f"""
        <html>
        <head>
            <title>Ultrasonic Sensor</title>
            <script>
                function changeValue(value)\u007b
                    var request = new XMLHttpRequest();
                    request.open("GET", "/servo/"+value, false);
                    request.send(null);
                    if (request.status === 200) \u007b
                        console.log(request.responseText);
                        document.getElementById('rangeValue').textContent = request.responseText;
                    \u007d
                \u007d
            </script>
        </head>
        <body>
            <h1>Servo Motor</h1>
            <center>
                <input type="range" min="5" max="10" step="0.25" value="7.25" style="width:80%;" onchange="changeValue(this.value)">
                <p id="rangeValue" style="font-size:32px;">7.25</p>
            </center>
        </body>
        </html>
        """
    return html

@app.route('/servo/<value>')
def servo_value(value):
    value = float(value)
    servo_pwm.ChangeDutyCycle(value)
    lcd.custom_rectangle(st7735_custom.BLACK, st7735_custom.BLACK)
    text = f"{value}"
    if(value<7):
        text=f"{value} (+90°)"
    elif(value>7.5):
        text=f"{value} (-90°)"
    else:
        text = f"{value}"
    lcd.custom_text(text=text)
    lcd.image()
    return text