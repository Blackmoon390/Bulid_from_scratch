import numpy as np #just used numpy for exponential function and max

class nn():
    def __init__(self,input_layer,hidden_layer,output_layer,lr=0.001):
        np.random.seed(42)
        self.input_layer=input_layer
        self.hidden_layer=hidden_layer
        self.output_layer=output_layer
        self.lr=lr

        self.w1=np.random.randn(self.input_layer,self.output_layer)*0.1
        self.b1=np.zeros(1,self.hidden_layer)
        
        
