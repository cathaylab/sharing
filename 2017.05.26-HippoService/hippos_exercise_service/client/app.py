from __future__ import print_function
from submitter import *
import SimpleHTTPServer
import SocketServer
import sys

PORT = 8000

if __name__ == '__main__':
	print('Start kafka consumer...')
	config = {
		'hippo_name': 'hippos_exercise_service',
		'sub_topics': ['frontier-adw'], 
		'pub_topic': 'hippo-finish',
		'kafka_host': 'localhost:9092',
		'job_script': '/Users/roger19890107/Developer/main/projects/cathay/DTAG-sharing/2017.05.26-HippoService/hippos_exercise_service/spark/submit.sh'
	}
	submitter = BasicSubmitter(config)
	submitter.start()

	# == start a server ==
	#input("Wait for message...")
	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer(("", PORT), Handler)
	print("serving client app at port: {}".format(PORT))
	httpd.serve_forever()
