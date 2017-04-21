import json

from kafka import KafkaConsumer
from kafka import KafkaProducer

class Worker(object):
    def __init__(self, topic, hosts="127.0.0.1:9092", group="testing", zookeeper_hosts="127.0.0.1:2181"):
        self.topic = topic
        self.consumer = KafkaConsumer(topic, bootstrap_servers=hosts)
        self.producer = KafkaProducer(bootstrap_servers=hosts)
    
    def run(self):
        for message in self.consumer:
            request = json.loads(message.value)
            
            self.process(request)
            
            # TODO: do something to submit the next task to the next worker automatically
            # self.producer.send(...)
            
    def process(self, request):
        request["ret"].append(self.topic)
        
        print request
        
worker = Worker("RC.Test")
worker.run()