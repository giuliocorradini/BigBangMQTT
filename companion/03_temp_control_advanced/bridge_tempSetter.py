import paho.mqtt.client as mqtt
import serial
import time
import logging

class CustomMQTTClient(mqtt.Client):
    topic = "5h/corradini"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial = serial.Serial("/dev/cu.usbmodem141203", baudrate=9600, bytesize=8, stopbits=1)
        self.last_t = "0.0"


    def on_connect(self, mqttc, obj, flags, rc):
        logging.info("Connected to server with return code {}".format(rc))

    def on_publish(self, mqttc, obj, mid):
        logging.debug("Published with message id {}".format(mid))

    def on_disconnect(self, mqttc, userdata, rc):
        if rc != 0:
            logging.warning("Unexpected disconnection from server. Result code {}".format(rc))
        logging.info("Successfully disconnected from server")

        self.serial.close()

    def send_temperature(self):
        temp = self.serial.readline()[:-1]
        logging.debug(temp)

        if temp == b"min":
            self.publish(f"{self.topic}/tmin", self.last_t, retain=True)
        elif temp == b"max":
            self.publish(f"{self.topic}/tmax", self.last_t, retain=True)
        elif temp == b"on" or temp == b"off":
            self.publish(f"{self.topic}/switch", temp)
        else:
            self.last_t = temp
            self.publish(f"{self.topic}/temp", temp)



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