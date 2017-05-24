from __future__ import print_function

import os
import subprocess
from threading import Thread
import time
import json

from kafka import KafkaConsumer, KafkaProducer


class BasicSubmitter(Thread):
	daemon = True

	def __init__(self, config):
		Thread.__init__(self)

		# config
		self.hippo_name = config['hippo_name']
		self.sub_topics = config['sub_topics']
		self.pub_topic = config['pub_topic']
		self.kafka_host = config['kafka_host']
		self.job_script = config['job_script']

		# producer
		self.producer = KafkaProducer(bootstrap_servers=self.kafka_host)


	def start_consumer(self):
		self.consumer = KafkaConsumer(bootstrap_servers=self.kafka_host,
								 	  auto_offset_reset='latest',
								 	  group_id=self.hippo_name)
		self.consumer.subscribe(self.sub_topics)


	def pub_job_result(self, code):
		pub_obj = {
			'hippo_name': self.hippo_name,
			'job_name': 'easy spark submit job',
			'is_success': code == 0,
			'finish_time': int(time.time())
		}
		pub_msg = json.dumps(pub_obj) # dict to json string
		print(pub_msg)
		self.producer.send(self.pub_topic, pub_msg)


	def submit_job(self):
		print('Start submitting spark job result...')
		code = subprocess.call([
			'/bin/sh',
			self.job_script
		])
		self.pub_job_result(code)


	def should_submit(self, message):
		return message.value == "submit"


	def run(self):
		while True:
			self.start_consumer()
			for message in self.consumer:
				if self.should_submit(message)
					self.consumer.close()
					self.submit_job()
					break


		

