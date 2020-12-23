import numpy as np
import scipy.ndimage
import dill as pickle
from ANNClass import BPNeuralNetwork

##########
#Test algorithm on small set
# numNodes = [784,100,10]
# n = BPNeuralNetwork(numNodes = numNodes, learningRate = 0.1, epochs = 5)
#
# data_file = open("smalltrain.csv",'r')
# data_list = data_file.readlines()
# data_file.close()
#
# for record in data_list:
#     record = record[1: (len(record) - 2)]
#     all_value = record.split(",")
#     scaled_input = (np.asfarray(all_value[1:])/255.0 * 0.99) + 0.01
#     targets = np.zeros(10) + 0.01
#     targets[int(all_value[0])] = 0.99
#     n.trainANN(scaled_input, targets)
#
# test_data_file = open("smalltest.csv", "r")
# test_data_list = test_data_file.readlines()
# test_data_file.close()
#
# score = [0,0]
# for trecord in test_data_list:
#     trecord = trecord[1 : (len(trecord) - 2)]
#     tall_value = trecord.split(",")
#     tvalue = int(tall_value[0])
#     pvalue = np.argmax(n.testANN((np.asfarray(tall_value[1:])/255.0 * 0.99) + 0.01))
#     if(tvalue == pvalue):
#         score[0] += 1
#     score[1] += 1

#############################################
#
numNodes = [784,200,10]
n = BPNeuralNetwork(numNodes = numNodes, learningRate = 0.1, epochs = 5)


data_file = open("mnist_train.csv",'r')
data_list = data_file.readlines()
data_file.close()
for e in range(n.epoch):
    for record in data_list:
        record = record[0: (len(record) - 1)]
        all_value = record.split(",")
        scaled_input = (np.asfarray(all_value[1:])/255.0 * 0.99) + 0.01
        targets = np.zeros(10) + 0.01
        targets[int(all_value[0])] = 0.99
        n.trainANN(scaled_input, targets)
        ## rotations
        inputs_plusx_img = scipy.ndimage.interpolation.rotate(scaled_input.reshape(28,28), 10, cval=0.01, order=1, reshape=False)
        n.trainANN(inputs_plusx_img.reshape(784), targets)
        # rotated clockwise by x degrees
        inputs_minusx_img = scipy.ndimage.interpolation.rotate(scaled_input.reshape(28,28), -10, cval=0.01, order=1, reshape=False)
        n.trainANN(inputs_minusx_img.reshape(784), targets)





test_data_file = open("mnist_test.csv", "r")
test_data_list = test_data_file.readlines()
test_data_file.close()


score = [0,0]
for trecord in test_data_list:
    trecord = trecord[0 : (len(trecord) - 1)]
    tall_value = trecord.split(",")
    tvalue = int(tall_value[0])
    pvalue = np.argmax(n.testANN((np.asfarray(tall_value[1:])/255.0 * 0.99) + 0.01))
    if(tvalue == pvalue):
        score[0] += 1
    score[1] += 1

print(score[0]/score[1])

with open('ann.pickle', 'wb') as handle:
    pickle.dump(n, handle, protocol=pickle.HIGHEST_PROTOCOL)
