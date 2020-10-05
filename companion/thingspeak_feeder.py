import logging

import paho.mqtt.client as mqtt
import requests

class MQTTClient(mqtt.Client):
    topic = "5h/corradini/temp"
    api_key = "5MMJ62YNEZWYYOD7"
    thingspeak_url = "https://api.thingspeak.com/update"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.measures = []

    def on_connect(self, mqttc, obj, flags, rc):
        logging.info("Connected to server with return code {}".format(rc))
        mqttc.subscribe(MQTTClient.topic)

    def on_disconnect(self, userdata, rc):
        if rc != 0:
            logging.warning("Unexpected disconnection from server. Result code {}".format(rc))
        logging.info("Successfully disconnected from server")

    def on_message(self, mqttc, userdata, msg):
        logging.debug(msg.payload)
        try:
            self.measures.append(float(msg.payload))
        except ValueError:
            logging.warning("Serial line received an invalid measure. Check connection")

        if len(self.measures) >= 4:
            self.send_temperature()

    def send_temperature(self):
        mean = sum(self.measures[:4]) / 4
        query = { 'api_key' : MQTTClient.api_key, 'field1' : mean }
        r = requests.get(MQTTClient.thingspeak_url, params=query)
        if r:
            logging.debug("Successfully sent mean temperature")
        else:
            logging.error("There was an error while sending a msg. {}".format(r.text))

        del self.measures[:4]


def main():
    client = MQTTClient("Corradini", protocol=mqtt.MQTTv311)

    client.connect("mqtt.ssh.edu.it")
    logging.info("Connected to MQTT server")

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()