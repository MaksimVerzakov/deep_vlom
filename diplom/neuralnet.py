from ffnet import ffnet, mlgraph, savenet, loadnet
from backend import TextBase

class NeuralNet(object):
    def __init__(self, layer_list):
        print 'Creating net'
        conec = mlgraph(layer_list)
        self.net = ffnet(conec)
        #self.load('new1.net')
        #print 'saved'

    def train(self, input, target):
        print "FINDING STARTING WEIGHTS WITH GENETIC ALGORITHM..."
        self.net.train_genetic(input, target, individuals=20,
                               generations=500)
        #then train with scipy tnc optimizer
        print "TRAINING NETWORK..."
        self.net.train_tnc(input, target, maxfun = 1000, messages=1)
        self.save('net_%s.net' % len(input))
        self._test(input, target)

    def _test(self, input, target):
        # Test network
        print "TESTING NETWORK..."
        output, regression = self.net.test(input, target, iprint = 2)

    def save(self, name):
        savenet(self.net, name)

    def load(self, path):
        self.net = loadnet(path)
