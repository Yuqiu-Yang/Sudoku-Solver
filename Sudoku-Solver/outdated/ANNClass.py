import numpy as np
import scipy.special

# define Neural Network Class
class BPNeuralNetwork(object):
    def __init__(self, numLayers = 3, numNodes = [3,2,1], learningRate = 0.1, epochs = 1):
        self.nLayer = numLayers
        self.nNodes = numNodes
        self.lRate = learningRate
        self.epoch = epochs
        self.activation = lambda x: scipy.special.expit(x)
        # weights stores link weights matrices
        # the length of weights should be nLayer - 1
        self.weights = []
        # outputs contains outputs of all hidden layers, 
        # the output of the final layer, and the initial input
        # the output of the first layer is the input
        self.outputs = []
        self.outputs.append(np.zeros([self.nNodes[0], 1]))
        # error contains distributed across all layers
        # including the final layer and the input layer
        self.error = []
        self.error.append(np.zeros([self.nNodes[0], 1]))
        ##############################################
        # Initialize the list of weights matrices
        for i in range(0, self.nLayer - 1):
            temp = np.random.normal(loc = 0.0, scale = pow(self.nNodes[i + 1], -0.5), size = (self.nNodes[i + 1], self.nNodes[i]))
            self.weights.append(temp)
        del temp
        # Initialize the list of output 
        for i in range(1, self.nLayer):
            temp = np.zeros([self.nNodes[i],1])
            self.outputs.append(temp)
        del temp
        # Initialize the list of error
        for i in range(1, self.nLayer):
            temp = np.zeros([self.nNodes[i],1])
            self.error.append(temp)
        del temp
        
    def forward_propagation(self, imageInputRowVector):
        self.outputs[0] = np.array(imageInputRowVector, ndmin = 2).T
        for i in range(1, self.nLayer):
            self.outputs[i] = np.dot(self.weights[i - 1], self.outputs[i - 1])
            self.outputs[i] = self.activation(self.outputs[i])
        return self.outputs
        
    def backward_propagation(self, trueValueRowVector):
        trueOutputs = np.array(trueValueRowVector, ndmin = 2).T
        self.error[-1] = trueOutputs - self.outputs[-1] 
        for i in range(self.nLayer - 2, -1, -1):
            self.error[i] = np.dot(self.weights[i].T, self.error[i + 1])
            temp1 = self.error[i + 1] * self.outputs[i + 1] * (1.0 - self.outputs[i + 1])
            temp2 = np.transpose(self.outputs[i])
            self.weights[i] += self.lRate * np.dot(temp1, temp2)
        pass
    def trainANN(self, imageInputRowVector, trueValueRowVector):
        self.forward_propagation(imageInputRowVector)
        self.backward_propagation(trueValueRowVector)
        pass
    def testANN(self, imageInputRowVector):
        self.forward_propagation(imageInputRowVector)
        return self.outputs[-1]
