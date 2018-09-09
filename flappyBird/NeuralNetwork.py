import math, json
from matrix import *

def sigmoid(x):
    return 1 / (1+ math.exp(-x))

def dsigmoid(y):
    #return sigmoid(x) * (1- sigmoid(x))
    return y * (1 - y)

class NeuralNetwork:
    def __init__(self, numI_, numH_ = None, numO_ = None, learning_rate_ = 0.1):
        if isinstance(numI_, NeuralNetwork):
            self.numI = numI_.numI
            self.numH = numI_.numH
            self.numO = numI_.numO

            self.weights_ih = numI_.weights_ih.copy()
            self.weights_ho = numI_.weights_ho.copy()
            self.bias_h = numI_.bias_h.copy()
            self.bias_o = numI_.bias_o.copy()
            self.learning_rate = numI_.learning_rate

        else:
            self.numI = numI_
            self.numH = numH_
            self.numO = numO_
            self.weights_ih = Matrix(self.numH, self.numI)
            self.weights_ho = Matrix(self.numO, self.numH)
            self.weights_ih.randomize()
            self.weights_ho.randomize()

            self.bias_h = Matrix(self.numH, 1)
            self.bias_h.randomize()
            self.bias_o = Matrix(self.numO, 1)
            self.bias_o.randomize()

            self.learning_rate = learning_rate_

    def setLearning_rate(self, value):
        self.learning_rate = value
        
    def feedforward(self, input_array):
        # generating the hidden Layer
        inputs = Matrix.fromArray(input_array)
        hidden = Matrix.multiply(self.weights_ih, inputs)
        hidden.add(self.bias_h)
        hidden.map(sigmoid)
        # generating the output layer
        output = Matrix.multiply(self.weights_ho, hidden)
        output.add(self.bias_o)
        output.map(sigmoid)
        # return the answer as array
        return output.toArray()

    def train(self, inputs_arr, targets_arr):
        inputs = Matrix.fromArray(inputs_arr)
        hidden = Matrix.multiply(self.weights_ih, inputs)
        hidden.add(self.bias_h)
        hidden.map(sigmoid)
        # generating the output layer
        outputs = Matrix.multiply(self.weights_ho, hidden)
        outputs.add(self.bias_o)
        outputs.map(sigmoid)

        targets = Matrix.fromArray(targets_arr)
        output_errors = Matrix.subtract(targets, outputs)
        # calc gradients
        gradients = Matrix.static_map(outputs, dsigmoid)
        gradients.scale(output_errors)
        gradients.scale(self.learning_rate)
        # calc deltas
        hidden_T = Matrix.transpose(hidden)
        weights_ho_deltas = Matrix.multiply(gradients, hidden_T)

        self.weights_ho.add(weights_ho_deltas)
        self.bias_o.add(gradients)
        
        who_t = Matrix.transpose(self.weights_ho)
        hidden_errors = Matrix.multiply(who_t, output_errors)
        # calc gradients
        hidden_gradient = Matrix.static_map(hidden, dsigmoid)
        hidden_gradient.scale(hidden_errors)
        hidden_gradient.scale(self.learning_rate)
        #calc deltas
        inputs_T = Matrix.transpose(inputs)
        weights_ih_deltas = Matrix.multiply(hidden_gradient, inputs_T)

        self.weights_ih.add(weights_ih_deltas)
        self.bias_h.add(hidden_gradient)

    def mutate(self, rate):
        def muta(val):
            if random.random() < rate:
                offset = random.gauss(0, 1) * 0.5
                newval = val + offset
                return newval
            else:
                return val
        self.weights_ih.map(muta)
        self.weights_ho.map(muta)
        self.bias_h.map(muta)
        self.bias_o.map(muta)

    def save(self, path):
        data = []
        data.append(self.weights_ih.__dict__)
        data.append(self.weights_ho.__dict__)
        data.append(self.bias_h.__dict__)
        data.append(self.bias_o.__dict__)
        with open(path, 'w') as outfile:
            json.dump(data, outfile)

    def load(self, path):
        with open(path) as infile:
            data = json.load(infile)
            self.weights_ih = Matrix.dataToMatrix(data[0])
            self.weights_ho = Matrix.dataToMatrix(data[1])
            self.bias_h = Matrix.dataToMatrix(data[2])
            self.bias_o = Matrix.dataToMatrix(data[3])
        print('Loading Brain successfull')

    def copy(self):
        return NeuralNetwork(self)

    def crossover(self, other):
        result = NeuralNetwork(self.numI, self.numH, self.numO)

        for i in range(0, 8, 2):
            randI = random.randint(0, 1) + i
            if randI is 0:
                result.weights_ih = self.weights_ih
            elif randI is 1:
                result.weights_ih = other.weights_ih
            elif randI is 2:
                result.weights_ho = self.weights_ho
            elif randI is 3:
                result.weights_ho = other.weights_ho
            elif randI is 4:
                result.bias_h = self.bias_h
            elif randI is 5:
                result.bias_h = other.bias_h
            elif randI is 6:
                result.bias_o = self.bias_o
            elif randI is 7:
                result.bias_o = other.bias_o
            else:
                print('You created useless numbers')

        return result
            
