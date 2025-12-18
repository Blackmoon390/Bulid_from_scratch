import numpy as np #just used numpy for exponential function and max
import pandas as pd # for split  training set ,test set

class nn():
    def __init__(self,input_layer,hidden_layer,output_layer,lr=0.001):
        np.random.seed(42)
        self.input_layer=input_layer
        self.hidden_layer=hidden_layer
        self.hidden_layer2=8
        self.output_layer=output_layer
        self.lr=lr

        self.w1=np.random.randn(self.input_layer,self.hidden_layer)*0.1
        self.b1=np.zeros((1,self.hidden_layer))

        self.w2=np.random.randn(self.hidden_layer,self.hidden_layer2)*0.1
        self.b2=np.zeros((1,self.hidden_layer2))

        self.w3=np.random.randn(self.hidden_layer2,self.output_layer)*0.1
        self.b3=np.zeros((1,self.output_layer))

    def relu(self,z):
        return np.max(z,0)
    
    def relu_derivative(self,z):
        return (z > 0).astype(float)
    
    def sigmoid(self,z):
        return 1/(1+np.exp(-z))
    
    def forward(self,x):
        self.z1=x@self.w1+self.b1
        self.a1=self.relu(self.z1)
        print(self.a1)

        self.z2=self.a1@self.w2+self.b2
        self.a2=self.relu(self.z2)
        print(self.a2)

        self.z3=self.a2@self.w3+self.b3
        self.y_pred=self.sigmoid(self.z3)

        return self.y_pred

 
hello=nn(2,3,1)
array=np.array([[23,5]])

print(hello.forward(array))
        
