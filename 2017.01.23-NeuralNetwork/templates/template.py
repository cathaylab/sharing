# To support both python 2 and python 3
from __future__ import division, print_function, unicode_literals

# Common imports
import numpy as np
import tensorflow as tf


# initialize variables/model parameters


# define the training phase operations
def inference(X):
	# how to in inference model over data X and predict Y
	pass


def loss(X, Y):
	# loss function. ex: MSE, Cross Entropy...
	pass


def inputs():
	# read or make training data	
	pass


def train(total_loss):
	# training operation
	pass


def evaluate(sess, X, Y):
	# evaluate current performance. ex: accuracy
	pass

# before 0.12
init = tf.initialize_all_variable()
# after 0.12
#init tf.global_variables_initializer().run()

# Create a saver to save model
saver = tf.train.Saver()
model_path = "../tf/models/XXX/prefix"


with tf.Session() as sess:
	sess.run(init)

	# get inputs
	X, Y = inputs()

	# get traing operation that will minimize the loss
	total_loss = loss(X, Y)
	train_op = train(total_loss)

	# prepare multi threads env
	coord = tf.train.Coordinator()
	threads = tf.train.start_queue_runners(sess=sess, coord=coord)

	## actual training 
	training_steps = 1000
	for step in range(training_steps):
		sess.run(train_op)
		# check loss
		if step % 10 == 0:
			print("loss", sess.run(total_loss))
		# save temp model 
		if step % 1000 == 0:
			saver.save(sess, model_path, global_step=step)

	# evaluate performance with test data
	evaluate(sess, X, Y)

	# save final model
	saver.save(sess, model_path, global_step=training_steps)

	# stop threads
	coord.request_stop()
	coord.join(threads)
	
	# close session
	sess.close()




