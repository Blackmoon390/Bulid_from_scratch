import numpy as np #just used numpy for exponential function and max
import pandas as pd # for split  training set ,test set

class nn():
    def __init__(self,lr=0.001,epoch=3000):
        
    
    
    def sigmoid(self,z):
        return 1/(1+np.exp(-z))
    
    
  
    def loss(self, y):
        eps = 1e-9
        return -np.mean(y*np.log(self.y_pred+eps) +
                        (1-y)*np.log(1-self.y_pred+eps))
        


 
data=pd.read_csv("dataset2.csv")

x=data.drop(columns=["motor"]).to_numpy()
y=data["motor"].to_numpy().reshape(-1,1)

print(x.shape,y.shape)


network=nn(9,16,1,0.001)

for epoch in range(0,2000):
    network.forward(x)
    los=network.loss(y)
    if epoch%100 ==0:print(los)
    network.backpropagation(x,y)






        
