from ffnet import ffnet, mlgraph, savenet, loadnet, exportnetzz
from backend import TextBase

class NeuralNet(object):
    def __init__(self, layer_list):
        conec = mlgraph(layer_list)
        self.net = ffnet(conec)

    def train(self, dict):
        print "FINDING STARTING WEIGHTS WITH GENETIC ALGORITHM..."
        input = []
        target = []
        for el in dict:
            input.extend(dict(el))
            null_tar = [0 for x in range(len(dict))]
            null_tar[dict.keys().index(el)] = 1.0
            target.extend([null_tar for x in range(dict(el))])
        self.net.train_genetic(input, target, individuals=20,
                               generations=500)
        #then train with scipy tnc optimizer
        print "TRAINING NETWORK..."
        self.net.train_tnc(input, target, maxfun = 1000, messages=1)

    def _test(self, input, target):
        # Test network
        print "TESTING NETWORK..."
        output, regression = self.net.test(input, target, iprint = 2)

    def save(self):
        savenet(self.net, "xor.net")

    def load(self, path):
        self.net = loadnet(path)
