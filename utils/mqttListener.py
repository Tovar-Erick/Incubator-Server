import paho.mqtt.client as mqtt
import abc
import string
import random
import json

class myMqtt:

    def processMessage(self, topic, msgJson):
        '''Sensor or camera method dispatcher'''
        if topic == 'JICA/Plantitas/Sensors':
            self.processSensorMessage(msgJson)
        if topic == 'JICA/Plantitas/Camera':
            self.processCameraMessage(msgJson)
        return

    @property
    def processSensorMessage(self, message):
        raise NotImplementedError("Callback should be attached!")

    @property
    def processCameraMessage(self, message):
        raise NotImplementedError("Callback should be attached!")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(self.channel)
        else:
            raise RuntimeError('Error connecting to Adafruit IO with rc: {0}'.format(rc))

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")

    def on_message(self, client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        msgJson = json.loads(msg)
        self.processMessage(message.topic, msgJson)
        if msg == '-stop listener method-':
            print('I dont wanna live anymore!!')
            client.disconnect()

    def on_log(self, client, userdata, level, buf):
        print("log: ", buf)

    def __init__(self, channel, processSensorFunction, processCameraFunction):
        self.channel = channel
        print(self.channel)
        #TODO: Find a reliavable MQTT server...   https://github.com/mqtt/mqtt.github.io/wiki/public_brokers
        self.broker_address = 'test.mosquitto.org'#"iot.eclipse.org"

        self.port = 1883
        self.keepAlive = 60 #one minute
        self.client_name = ''.join(random.choice(string.lowercase) for iter in range(6))
        #New instance
        self.client = mqtt.Client(self.client_name)

        #Attach callbacks
        self.processSensorMessage = processSensorFunction
        self.processCameraMessage = processCameraFunction
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # self.client.on_log = self.on_log
        self.client.on_disconnect = self.on_disconnect

    def start_listening(self):
        self.client.connect(self.broker_address, self.port, self.keepAlive)
        self.client.loop_forever()
