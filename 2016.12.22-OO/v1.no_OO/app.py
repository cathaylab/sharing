#!/usr/bin/env python

import os
import click

from builder import IrisModelBuilder

root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

@click.command()
@click.option("--channels", required=True)
def run(channels):
    global root_dir

    service_name = 'iris_classifier'

    model_path = os.path.join(root_dir, "models", "iris_dnn")

    # start service
    iris_builder = IrisModelBuilder(model_path, channels=channels.split(","))
    iris_builder.build()
    iris_builder.run()

if __name__ == "__main__":
    run()
