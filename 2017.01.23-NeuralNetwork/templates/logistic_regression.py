# To support both python 2 and python 3
from __future__ import division, print_function, unicode_literals

# Common imports
import numpy as np
import tensorflow as tf
import os


# initialize variables/model parameters
W = tf.Variable(tf.zeros([5, 1]), name="weights")
b = tf.Variable(0., name="bias")


def combine_inputs(X):
	return tf.matmul(X, W) + b


# define the training phase operations
def inference(X):
	# how to in inference model over data X and predict Y
	return tf.sigmoid(combine_inputs(X))


def loss(X, Y):
	# loss function. Sigmoid + Cross Entropy...
	return tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits((combine_inputs(X)), Y))


def read_csv(batch_size, filename, record_defaults):
	filename_queue = tf.train.string_input_producer([filename])

	reader = tf.TextLineReader(skip_header_lines=1)
	key, value = reader.read(filename_queue)

	decoded = tf.decode_csv(value, record_defaults=record_defaults)

	return tf.train.shuffle_batch(decoded,
								  batch_size=batch_size,
								  capacity=batch_size*50,
								  min_after_dequeue=batch_size)


def inputs():
	# read or make training data	
	passengerId, survived, pclass, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked = \
		read_csv(100, 'titantic.csv', [[0.0], [0.0], [0], [""], [""], [0.0], [0.0], [0.0], [""], [0.0], [""], [""]])

	is_first_class = tf.cast(tf.equal(pclass, [1]), tf.float32)
	is_second_class = tf.cast(tf.equal(pclass, [2]), tf.float32)
	is_third_class = tf.cast(tf.equal(pclass, [3]), tf.float32)

	gender = tf.cast(tf.equal(sex, ["female"]), tf.float32)

	features = tf.pack([is_first_class, is_second_class, is_third_class, gender, age], axis=1)
	survived = tf.reshape(survived, [100, 1])
	
	return features, survived


def train(total_loss):
	# training operation
	learning_rate = 0.005
	return tf.train.GradientDescentOptimizer(learning_rate).minimize(total_loss)


def evaluate(sess, X, Y):
	# evaluate current performance. ex: accuracy
	predicted = tf.cast(inference(X) > 0.5, tf.float32)
	accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), tf.float32))
	print("accuracy: " + str(sess.run(accuracy)))


# before 0.12
#init = tf.initialize_all_variable()
# after 0.12
init = tf.global_variables_initializer()

# Create a saver to save model
saver = tf.train.Saver()
model_path = "models/logistic_regression/lg"

features, label = inputs()

# with tf.Session() as sess:
# 	sess.run(init)

# 	coord = tf.train.Coordinator()
# 	threads = tf.train.start_queue_runners(coord=coord)

# 	try:
# 		i = 0
# 		while not coord.should_stop() and i < 5:
# 			print(sess.run([features, label]))
# 			i += 1

# 	except tf.errors.OutOfRangeError:
# 		print("Done training -- epoch limit reached")

# 	finally:
# 		coord.request_stop()


# 	coord.join(threads)


with tf.Session() as sess:
	sess.run(init)

	# get inputs
	features, label = inputs()

	# get traing operation that will minimize the loss
	total_loss = loss(features, label)
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
	evaluate(sess, features, label)

	# save final model
	saver.save(sess, model_path, global_step=training_steps)

	# stop threads
	coord.request_stop()
	coord.join(threads)
	
	# close session
	sess.close()




