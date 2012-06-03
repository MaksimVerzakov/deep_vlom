from svm import *
from svmutil import *

class SVM(object):
    def __init__(self, input, target):
        self.prob = svm_problem(target, input)
        self.param = svm_parameter('-t 0 -c 0.5 -b 4')
        self.svm = libsvm.svm_train(self.prob, self.param)

    def predict(self, vector):
        x0, max_idx = gen_svm_nodearray(vector)
        return libsvm.svm_predict(self.svm, x0)
