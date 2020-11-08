import logging

import serial
import paho.mqtt.client as mqtt

class MQTTClient(mqtt.Client):

    def __init__(self, topic, serial_port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial = serial_port
        self.topic = f"5h/{topic}"

    def on_connect(self, mqttc, obj, flags, rc):
        logging.info("Connected to server with return code {}".format(rc))
        mqttc.subscribe(f"{self.topic}/temp")
        mqttc.subscribe(f"{self.topic}/tmax")
        mqttc.subscribe(f"{self.topic}/tmin")
        mqttc.subscribe(f"{self.topic}/switch")

        self.t_max = 28.5
        self.t_min = 27.5

    def on_disconnect(self, mqttc, userdata, rc):
        if rc != 0:
            logging.warning("Unexpected disconnection from server. Result code {}".format(rc))
        logging.info("Successfully disconnected from server")

    def on_message(self, mqttc, userdata, msg):
        logging.info(f"msg: {msg.payload.decode()} from topic: {msg.topic}")

        if "switch" in msg.topic:
            if msg.payload == b'off':
                self.serial.write(b'o')
            elif msg.payload == b'on':
                self.serial.write(b'f')
            else:
                logging.warning("Switch message not valid")

        else:
            try:
                temp = float(msg.payload.decode())

                if "tmax" in msg.topic:
                    self.t_max = temp
                elif "tmin" in msg.topic:
                    self.t_min = temp
                else:
                    if temp > self.t_max:
                        action = 'c'
                    elif temp < self.t_min:
                        action = 'h'
                    else:
                        action = 's'


                    response = ''
                    i=0
                    while response != action:
                        self.serial.write(action.encode())
                        try:
                            response = self.serial.read(1).decode()
                        except serial.SerialTimeoutException:
                            logging.info("Didn't receive a response\n")
                        if i == 10: break
                        i += 1

            except ValueError:
                logging.warning("Invalid temperature")

        


def main():
    with serial.Serial("/dev/cu.usbmodem141203") as s:
        logging.info("Serial port opened")

        client = MQTTClient(protocol=mqtt.MQTTv311, topic="corradini", serial_port=s)

        client.connect("mqtt.ssh.edu.it")
        logging.info("Connected to MQTT server")

        try:
            client.loop_forever()
        except KeyboardInterrupt:
            client.disconnect()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()