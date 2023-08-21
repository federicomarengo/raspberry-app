from flask import *
app = Flask(__name__)

import RPi.GPIO as GPIO
import time
#!/usr/bin/env python
import os
from flask_cors import CORS
cors = CORS(app)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpioList = [9, 2, 3, 4, 5, 6, 7, 8]

for i in gpioList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)


@app.route('/', methods=['GET'])
def check_status():
   return 'Everithing OK'

@app.route('/setPin', methods=['GET'])
def setPin():
   pin = request.args.get('pin', type = int)
   state = request.args.get('state', type = int)

   # here. The validation to check if the pin recived by parameters is contained in PigpioList
   if(state == 1):
      GPIO.output(pin, GPIO.LOW)
      return str(pin) + ' Encendido'
   else:
      GPIO.output(pin, GPIO.HIGH)
      return str(pin) + ' Apagado'

@app.route('/temperature', methods=['GET'])
def temperature():

   serialNum = sensor()

   if read(serialNum) != None:
      return "%0.1f" % read(serialNum)[0]
   else:
      return 0

def sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i
    return ds18b20

def read(ds18b20):
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    farenheit = (celsius * 1.8) + 32
    return celsius, farenheit


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8005, debug=True)