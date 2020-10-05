import logging

import paho.mqtt.client as mqtt

class MQTTClient(mqtt.Client):
    topic = "5h/+/temp"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_connect(self, mqttc, obj, flags, rc):
        logging.info("Connected to server with return code {}".format(rc))
        mqttc.subscribe(MQTTClient.topic)

    def on_disconnect(self, userdata, rc):
        if rc != 0:
            logging.warning("Unexpected disconnection from server. Result code {}".format(rc))
        logging.info("Successfully disconnected from server")

    def on_message(self, mqttc, userdata, msg):
        logging.info(f"msg: {msg.payload.decode()} from topic: {msg.topic}")


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