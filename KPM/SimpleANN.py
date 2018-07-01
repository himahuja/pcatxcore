import numpy as np

def sigmoid(x,deriv=False):
	if(deriv==True):
	    return x*(1-x)

	return 1/(1+np.exp(-x))
    
class two_layer_ANN(object):
    
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        # seed random numbers to make calculation
        # deterministic (just a good practice)
        np.random.seed(1)
        # initialize weights randomly with mean 0
        self.syn0 = 2*np.random.random((self.X.shape[1],self.Y.shape[1])) - 1
        
    def reset_synapses(self):
        np.random.seed(1)
        self.syn0 = 2*np.random.random((self.X.shape[1],self.Y.shape[1])) - 1

    def train(self, iterations):
        for j in range(iterations):
        
            # forward propagation
            l0 = self.X
            l1 = sigmoid(np.dot(l0,self.syn0))
        
            # how much did we miss?
            l1_error = self.Y - l1
            
            if (j % 10000) == 0:
                print("Error: " + str(np.mean(np.abs(l1_error))))
        
            # multiply how much we missed by the 
            # slope of the sigmoid at the values in l1
            l1_delta = l1_error * sigmoid(l1,True)
        
            # update weights
            self.syn0 += np.dot(l0.T,l1_delta)
        
        print("Output After Training:")
        print(l1)


class three_layer_ANN(object):
    
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        # randomly initialize our weights with mean 0
        np.random.seed(1)
        self.syn0 = 2*np.random.random((X.shape[1],X.shape[0])) - 1
        self.syn1 = 2*np.random.random((X.shape[0],Y.shape[1])) - 1
    
    def reset_synapses(self):
        np.random.seed(1)
        self.syn0 = 2*np.random.random((X.shape[1],X.shape[0])) - 1
        self.syn1 = 2*np.random.random((X.shape[0],Y.shape[1])) - 1
    
    def train(self, iterations):
        for j in range(iterations):
        
        	# Feed forward through layers 0, 1, and 2
            l0 = self.X
            l1 = sigmoid(np.dot(l0,self.syn0))
            l2 = sigmoid(np.dot(l1,self.syn1))
        
            # how much did we miss the target value?
            l2_error = self.Y - l2
            
            if (j% 10000) == 0:
                print("Error: " + str(np.mean(np.abs(l2_error))))
                
            # in what direction is the target value?
            # were we really sure? if so, don't change too much.
            l2_delta = l2_error*sigmoid(l2,deriv=True)
        
            # how much did each l1 value contribute to the l2 error (according to the weights)?
            l1_error = l2_delta.dot(self.syn1.T)
            
            # in what direction is the target l1?
            # were we really sure? if so, don't change too much.
            l1_delta = l1_error * sigmoid(l1,deriv=True)
        
            self.syn1 += l1.T.dot(l2_delta)
            self.syn0 += l0.T.dot(l1_delta)
           
        print("Output After Training:")
        print(l2)
        
class four_layer_ANN(object):
    
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        # randomly initialize our weights with mean 0
        np.random.seed(1)
        self.syn0 = 2*np.random.random((X.shape[1],X.shape[0])) - 1
        self.syn1 = 2*np.random.random((X.shape[0],X.shape[0])) - 1
        self.syn2 = 2*np.random.random((X.shape[0],Y.shape[1])) - 1
    
    def reset_synapses(self):
        np.random.seed(1)
        self.syn0 = 2*np.random.random((X.shape[1],X.shape[0])) - 1
        self.syn1 = 2*np.random.random((X.shape[0],X.shape[0])) - 1
        self.syn2 = 2*np.random.random((X.shape[0],Y.shape[1])) - 1
    
    def train(self, iterations):
        for j in range(iterations):
        
        	# Feed forward through layers 0, 1, and 2
            l0 = self.X
            l1 = sigmoid(np.dot(l0,self.syn0))
            l2 = sigmoid(np.dot(l1,self.syn1))
            l3 = sigmoid(np.dot(l2,self.syn2))
        
            # how much did we miss the target value?
            l3_error = self.Y - l3
            
            if (j% 10000) == 0:
                print("Error: " + str(np.mean(np.abs(l3_error))))
                
            # in what direction is the target value?
            # were we really sure? if so, don't change too much.
            l3_delta = l3_error*sigmoid(l3,deriv=True)
            l2_error = l3_delta.dot(self.syn2.T)
            l2_delta = l2_error*sigmoid(l2,deriv=True)
            l1_error = l2_delta.dot(self.syn1.T)
            l1_delta = l1_error*sigmoid(l1,deriv=True)
        
            self.syn2 += l2.T.dot(l3_delta)
            self.syn1 += l1.T.dot(l2_delta)
            self.syn0 += l0.T.dot(l1_delta)
           
        print("Output After Training:")
        print(l3)
        
class five_layer_ANN(object):
    
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        # randomly initialize our weights with mean 0
        np.random.seed(1)
        self.syn0 = 2*np.random.random((X.shape[1],X.shape[0])) - 1
        self.syn1 = 2*np.random.random((X.shape[0],X.shape[0])) - 1
        self.syn2 = 2*np.random.random((X.shape[0],X.shape[0])) - 1
        self.syn3 = 2*np.random.random((X.shape[0],Y.shape[1])) - 1
    
    def reset_synapses(self):
        np.random.seed(1)
        self.syn0 = 2*np.random.random((X.shape[1],X.shape[0])) - 1
        self.syn1 = 2*np.random.random((X.shape[0],X.shape[0])) - 1
        self.syn2 = 2*np.random.random((X.shape[0],X.shape[0])) - 1
        self.syn3 = 2*np.random.random((X.shape[0],Y.shape[1])) - 1
    
    def train(self, iterations):
        for j in range(iterations):
        
        	# Feed forward through layers 0, 1, and 2
            l0 = self.X
            l1 = sigmoid(np.dot(l0,self.syn0))
            l2 = sigmoid(np.dot(l1,self.syn1))
            l3 = sigmoid(np.dot(l2,self.syn2))
            l4 = sigmoid(np.dot(l3,self.syn3))
        
            # how much did we miss the target value?
            l4_error = self.Y - l4
            
            if (j% 10000) == 0:
                print("Error: " + str(np.mean(np.abs(l4_error))))
                
            # in what direction is the target value?
            # were we really sure? if so, don't change too much.
            l4_delta = l4_error*sigmoid(l4,deriv=True)
            l3_error = l4_delta.dot(self.syn3.T)
            l3_delta = l3_error*sigmoid(l3,deriv=True)
            l2_error = l3_delta.dot(self.syn2.T)
            l2_delta = l2_error*sigmoid(l2,deriv=True)
            l1_error = l2_delta.dot(self.syn1.T)
            l1_delta = l1_error*sigmoid(l1,deriv=True)
        
            self.syn3 += l3.T.dot(l4_delta)
            self.syn2 += l2.T.dot(l3_delta)
            self.syn1 += l1.T.dot(l2_delta)
            self.syn0 += l0.T.dot(l1_delta)
           
        print("Output After Training:")
        print(l4)
   
def main():
    X = np.array([[0,0,1],
            [0,1,1],
            [1,0,1],
            [1,1,1]])
                
    y = np.array([[0],
			[1],
			[1],
			[0]])
   
    ann = five_layer_ANN(X,y)
    ann.train(50000)
    
    
if __name__ == u"__main__" :
    main()



