from interface import MLBuilder

from algorithm import IrisDNN

class IrisModelBuilder(MLBuilder):
    def build_model(self):
        print("build iris model... ")

        # train model
        iris_dnn = IrisDNN(self.model_path)
        iris_dnn.train_model()
        iris_dnn.save_model()
