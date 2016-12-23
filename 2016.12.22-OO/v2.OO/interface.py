import redis

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EVENT_TRAIN = "BUILD_MODEL"

class MLListener(object):
    def __init__(self, r=None, channels=[]):
        if r is None:
            self.redis = redis.Redis()
        else:
            self.redis = r

        self.pubsub = self.redis.pubsub()

        if channels:
            self.subscribe(channels)

        self.channels = channels

    def get_channels(self):
        return self.channels

    def listen(self):
        for item in self.pubsub.listen():
            yield item

    def publish(self, channel, event):
        self.redis.publish(channel, event)

    def unsubscribe(self):
        self.pubsub.unsubscribe()
        logger.info('{} tries to unsubscribe the channelds successfully'.format(type(self).__name__))

    def subscribe(self, channels):
        self.pubsub.subscribe(channels)


class MLBuilder(object):
    def __init__(self, dataset_path, model_path, channels):
        self.model_path = model_path
        self.dataset_path = dataset_path
        self.channels = channels

        self.listener = MLListener(channels=channels)

    def build(self):
        raise NotImplementedError

    def run(self):
        print("Listen build {} model command...".format(self.listener.get_channels()))

        for item in self.listener.listen():
            if item['data'] == EVENT_TRAIN:
                self.build()
