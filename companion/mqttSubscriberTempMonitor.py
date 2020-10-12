import logging

import serial
import paho.mqtt.client as mqtt

class MQTTClient(mqtt.Client):

    def __init__(self, topic, serial_port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial = serial_port
        self.topic = f"5h/{topic}/temp"

    def on_connect(self, mqttc, obj, flags, rc):
        logging.info("Connected to server with return code {}".format(rc))
        mqttc.subscribe(self.topic)

        self.max_t = 28.0
        self.min_t = 27.0

    def on_disconnect(self, userdata, rc):
        if rc != 0:
            logging.warning("Unexpected disconnection from server. Result code {}".format(rc))
        logging.info("Successfully disconnected from server")

    def on_message(self, mqttc, userdata, msg):
        logging.info(f"msg: {msg.payload.decode()} from topic: {msg.topic}")
        try:
            temp = float(msg.payload.decode())
            if temp > self.max_t:
                action = 'c'
            elif temp < self.min_t:
                action = 'h'
            else:
                action = 's'

            response = ''
            while response != action:
                self.serial.write(action.encode())
                response = self.serial.read(1).decode()

        except ValueError:
            logging.warning("Invalid temperature")


def main():
    with serial.Serial("COM6") as s:
        client = MQTTClient(protocol=mqtt.MQTTv311, topic="fano", serial_port=s)

        client.connect("mqtt.ssh.edu.it")
        logging.info("Connected to MQTT server")

        try:
            client.loop_forever()
        except KeyboardInterrupt:
            client.disconnect()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()