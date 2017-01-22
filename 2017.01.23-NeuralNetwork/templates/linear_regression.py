# To support both python 2 and python 3
from __future__ import division, print_function, unicode_literals

# Common imports
import numpy as np
import tensorflow as tf


# initialize variables/model parameters
W = tf.Variable(tf.zeros([2, 1]), name="weights")
b = tf.Variable(0., name="bias")

# define the training phase operations
def inference(X):
	# how to in inference model over data X and predict Y
	return tf.matmul(X, W) + b


def loss(X, Y):
	# MSE
	Y_predicted = inference(X)
	return tf.reduce_mean(tf.square(Y - Y_predicted))


def inputs():
	weight_age = [[84, 46], [73, 20], [65, 52], [70, 30], [76, 57], [69, 25], [63, 28], [72, 36], [79, 57], [75, 44], [27, 24], [89, 31], [65, 52], [57, 23], [59, 60], [69, 48], [60, 34], [79, 51], [75, 50], [82, 34], [59, 46], [67, 23], [85, 37], [55, 40], [63, 30]]
	blood_fat_content = [354, 190, 405, 263, 451, 302, 288, 385, 402, 365, 209, 290, 346, 254, 395, 434, 220, 374, 308, 220, 311, 181, 274, 303, 244]

	return(tf.cast(weight_age, tf.float32), tf.cast(blood_fat_content, tf.float32))


def train(total_loss):
	learning_rate = 0.0000001
	return tf.train.GradientDescentOptimizer(learning_rate).minimize(total_loss)


def evaluate(sess, X, Y):
	# evaluate the resulting trained model
	print(sess.run(inference([[80., 25.]])))
	print(sess.run(inference([[65., 25.]])))


# before 0.12
#init = tf.initialize_all_variable()
# after 0.12
init = tf.global_variables_initializer()

# Create a saver to save model
saver = tf.train.Saver()
model_path = "models/linear_regression/lr"


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




