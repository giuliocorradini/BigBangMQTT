import logging

import paho.mqtt.client as mqtt

class MQTTClient(mqtt.Client):
    def __init__(self, topic, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.topic = topic

    def on_connect(self, mqttc, obj, flags, rc):
        logging.info("Connected to server with return code {}".format(rc))
        mqttc.subscribe(self.topic)

    def on_disconnect(self, userdata, rc):
        if rc != 0:
            logging.warning("Unexpected disconnection from server. Result code {}".format(rc))
        logging.info("Successfully disconnected from server")

    def on_message(self, mqttc, userdata, msg):
        mqttc.publish(thingspeak_topic, msg.payload)


def main():
    client = MQTTClient(protocol=mqtt.MQTTv311)

    client.connect("mqtt.ssh.edu.it")
    logging.info("Connected to MQTT server")

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()