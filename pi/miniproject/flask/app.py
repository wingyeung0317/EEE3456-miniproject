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

app = Flask(__name__)

if __name__=='__main__':
    app.run()

# DHT LCD
lcd = st7735_custom.ST7735( cs_pin = digitalio.DigitalInOut(board.CE0),
                            dc_pin = digitalio.DigitalInOut(board.D25),
                            reset_pin = digitalio.DigitalInOut(board.D24))

dht11 = DHT.DHT11(pin = 2)

GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)
pir_pin = 15

ultrasonic_echo_pin = 27
ultrasonic_trig_pin = 22

GPIO.setup(pir_pin, GPIO.IN)
moved = 0
sleep(2)      #give sensor to startup
pir_results = pd.DataFrame([],columns=["motion", "time"])
pir_plot = pir_results.copy()

dht_results = pd.DataFrame([],columns=["temperature", "humidity", "time"])
dht_plot = dht_results.copy()
pir_results = pd.DataFrame([],columns=["motion", "time"])
pir_plot = pir_results.copy()

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

    if result.is_valid():
        clear_output(wait=False)
        dht_results.loc[len(dht_results.index)] = [result.temperature, result.humidity, arrow.now(tz="+08:00").format()]
        
        dht_plot = dht_results.copy()
        dht_plot.time = dht_plot.time.apply(lambda x: arrow.get(x).format('YYYY-MM-DD HH:mm'))
        print(f"Temp: {dht_results.loc[len(dht_results.index)-1, 'temperature']} \n Hum: {dht_results.loc[len(dht_results.index)-1, 'humidity']}")
        # display(dht_results)
        plotdf = pd.concat([dht_plot, pir_plot], ignore_index=True)
        display(plotdf)
        plt.figure().set_figheight(7)
        sns.lineplot(x="time", y="temperature", data=dht_plot)
        sns.lineplot(x="time", y="humidity", data=dht_plot)
        plt.yticks(np.arange(0, 101, 2))
        
        __tmpfiledht = BytesIO()
        plt.savefig(__tmpfiledht, format='png')
        __encoded = base64.b64encode(__tmpfiledht.getvalue()).decode('utf-8')
        imghtml = '<img class="pltimg" src=\'data:image/png;base64,{}\'>'.format(__encoded)
        plt.close()

        # plot = plt.show()

        # # lcd.custom_rectangle(color1=st7735_custom.BLACK, color2=st7735_custom.WHITE)
        # # lcd.__image = Image.open(__tmpfile).rotate(0).resize((lcd.width, lcd.height))
        # lcd.custom_img("dht_plot.jpg")
        # lcd.custom_text(text=f"Temp: {dht_results.loc[len(dht_results.index)-1, 'temperature']} \n Hum: {dht_results.loc[len(dht_results.index)-1, 'humidity']}", color=st7735_custom.RED)
        # lcd.image()
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
                    <h1>Temperature and Humidity</h1>
                    {imghtml}
                    <p>Temp: {dht_results.loc[len(dht_results.index)-1, 'temperature']}</p>
                    <p>Hum: {dht_results.loc[len(dht_results.index)-1, 'humidity']}</p>
                    {dht_results.to_html()}
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
    imghtml = '<img class="pltimg" src=\'data:image/png;base64,{}\' style="width:65%;float:left;">'.format(__encoded)
    plt.close()

    # plot = plt.show()

    # # lcd.custom_rectangle(color1=st7735_custom.BLACK, color2=st7735_custom.WHITE)
    # # lcd.__image = Image.open(__tmpfile).rotate(0).resize((lcd.width, lcd.height))
    # lcd.custom_img("plot.jpg")
    # lcd.custom_text(text=f"Temp: {dht_results.loc[len(dht_results.index)-1, 'temperature']} \n Hum: {dht_results.loc[len(dht_results.index)-1, 'humidity']}", color=st7735_custom.RED)
    # lcd.image()
    html = f"""
            <html>
            <head>
                <title>PIR</title>
                <script>
                    setTimeout(function()\u007b
                        location.reload();
                    \u007d, 50);
                </script>
            </head>
            <body>
                <h1>PIR</h1>
                {imghtml}
                <div style="width:34%; float:right;">
                    <span style="width:49%; float:left">{countdf.to_html()}</span>
                    <span style="width:49%; float:right">{pir_results.to_html()}</span>
                </div>
            </body>
            </html>
            """
    return html