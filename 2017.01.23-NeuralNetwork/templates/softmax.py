import tensorflow as tf
import os

W = tf.Variable(tf.zeros([4, 3]), name="weights")
b = tf.Variable(0., name="bias")

def combine_inputs(X):
    return tf.matmul(X, W) + b

def inference(X):
    return tf.nn.sigmoid(combine_inputs(X))

def loss(X, Y):
    return tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(combine_inputs(X), Y))

def read_csv(batch_size, filename, record_defaults):
    filname_queue = tf.train.string_input_producer([os.path.dirname(__file__) + "/datasets/" + filename])

    reader = tf.TextLineReader(skip_header_lines=1)
    key, value = reader.read(filname_queue)

    decoded = tf.decode_csv(value, record_defaults=record_defaults)

    return tf.train.shuffle_batch(decoded,
                                  batch_size=batch_size,
                                  capacity=batch_size * 50,
                                  min_after_dequeue=batch_size)

def inputs():
    sepal_length, sepal_width, petal_length, petal_width, label = \
        read_csv(100, 'iris.data', [[0.0], [0.0], [0.0], [0.0], [""]])

    # convert class names to a 0 based class index.
    label_number = tf.to_int32(tf.arg_max(tf.to_int32(tf.pack([
        tf.equal(label, ["Iris-setosa"]),
        tf.equal(label, ["Iris-versicolor"]),
        tf.equal(label, ["Iris-virginica"])
    ])), 0))

    features = tf.transpose(tf.pack([sepal_length, sepal_width, petal_length, petal_width]))

    return features, label_number

def train(total_loss):
    learning_rate = 0.01
    return tf.train.GradientDescentOptimizer(learning_rate).minimize(total_loss)

def evaluate(sess, X, Y):
    predicted = tf.cast(tf.arg_max(inference(X), 1), tf.int32)
    accuracy = sess.run(tf.reduce_mean(tf.cast(tf.equal(predicted, Y), tf.float32)))
    print("accuracy: " + str(accuracy))

# Launch the graph in a session, setup boilerplate
with tf.Session() as sess:

    tf.initialize_all_variables().run()

    X, Y = inputs()

    total_loss = loss(X, Y)
    train_op = train(total_loss)

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    # actual training loop
    training_steps = 1000
    for step in range(training_steps):
        sess.run([train_op])
        if step % 10 == 0:
            loss = sess.run([total_loss])
            print("%s. loss: %s" % (step, str(loss)))

    evaluate(sess, X, Y)

    coord.request_stop()
    coord.join(threads)
    sess.close()
