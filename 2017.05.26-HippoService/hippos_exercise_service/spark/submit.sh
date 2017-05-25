#!/usr/bin/env bash

#export SPARK_HOME=...

export APP_DIR=${PWD}
spark-submit ${PWD}/spark/app.py
