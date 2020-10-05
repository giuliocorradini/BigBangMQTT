import paho.mqtt.client as mqtt
import serial
import time
import logging

class CustomMQTTClient(mqtt.Client):
    topic = "5h/corradini/temp"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial = serial.Serial("COM6", baudrate=9600, bytesize=8, stopbits=1)


    def on_connect(self, mqttc, obj, flags, rc):
        logging.info("Connected to server with return code {}".format(rc))

    def on_publish(self, mqttc, obj, mid):
        logging.debug("Published with message id {}".format(mid))

    def on_disconnect(self, userdata, rc):
        if rc != 0:
            logging.warning("Unexpected disconnection from server. Result code {}".format(rc))
        logging.info("Successfully disconnected from server")

        self.serial.close()

    def send_temperature(self):
        temp = self.serial.readline()[:-1]
        logging.debug(temp)
        self.publish(self.topic, temp)



def main():
    client = CustomMQTTClient(protocol=mqtt.MQTTv311)

    client.connect("mqtt.ssh.edu.it")
    try:
        while True:
            client.send_temperature()

    except KeyboardInterrupt:
        pass

    client.disconnect()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()