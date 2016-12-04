#!/usr/bin/python

import sys

import numpy as np
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid

from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

from Queue import Queue
from threading import Thread

queue = Queue()

#unit_x, unit_y = 0.000001, 0.000001
unit_x, unit_y = 20, 40

location = int(sys.argv[1])

dataset = pd.read_csv("../dataset/train_sample_{}.csv".format(location))

size_x, size_y = 10.0/unit_x, 10.0/unit_y
pos_x, pos_y = dataset.x.values / size_x, dataset.y.values / size_y
grid_id = pos_y*size_x + pos_x

dataset["grid_id"] = grid_id.astype(np.int)

initial_date = np.datetime64('2014-01-01T01:01', dtype='datetime64[m]')
d_times = pd.DatetimeIndex(initial_date + np.timedelta64(int(mn), 'm') for mn in dataset.time.values)
dataset['hour'] = d_times.hour
dataset['weekday'] = d_times.weekday
dataset['day'] = d_times.dayofyear
dataset['month'] = d_times.month
dataset['year'] = (d_times.year - 2013)

def validate(n_folds=3):
    global dataset

    kf = KFold(n_splits=n_folds)

    while True:
        grid_cell = queue.get()

        matching = dataset.grid_id == grid_cell

        X = np.delete(dataset[matching].values, [0, 3, 4, 5, 6], axis=1)
        Y = dataset[matching]["place_id"].values

        #fw = [500, 1000, 4, 3, 1./22., 2, 10]
        #for idx, weight in enumerate(fw):
        #    X[:, idx] = X[:, idx]*weight
        print X[0]

        accuracy = [[], [], []]
        for sub_train, sub_test in kf.split(X):
            for idx, clf in enumerate([NearestCentroid(), KNeighborsClassifier(weights='uniform'), KNeighborsClassifier(weights="distance")]):
                clf.fit(X[sub_train], Y[sub_train])
                accuracy[idx].append(accuracy_score(Y[sub_test], clf.predict(X[sub_test])))

        print "The results of grid-{} is {}".format(grid_cell, [np.mean(a) for a in accuracy])

        queue.task_done()

for grid_cell in dataset["grid_id"].unique():
    queue.put((grid_cell))

for i in range(8):
    t = Thread(target=validate)
    t.daemon = True
    t.start()

queue.join()
