from libsvm import *

class SVM(object):
    def __init__(self, input, target):
        self.prob = svm_problem(target, input)
        self.param = svm_parameter(kernel_type = LINEAR, C = 10)
        ## training  the model
        self.svm = svm_model(self.prob, self.param)
        #testing the model

    def predict(self, vector)
        self.svm.predict(vector)
