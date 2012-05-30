import os, sys

from svm import *
from svmutil import *

class SVM(object):
    def __init__(self, input, target):
        self.prob = svm_problem(target, input)
        self.param = svm_parameter('-t 0 -c 4 -b 1')
        ## training  the model
        self.svm = libsvm.svm_train(self.prob, self.param)
        #testing the model

    def predict(self, vector):
        x0, max_idx = gen_svm_nodearray(vector)
        return libsvm.svm_predict(self.svm, x0)
