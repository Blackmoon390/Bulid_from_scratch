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
        return np.maximum(z,0)
    
    def relu_derivative(self,z):
        return (z > 0).astype(float)
    
    def sigmoid(self,z):
        return 1/(1+np.exp(-z))
    
    def forward(self,x):
        self.z1=x@self.w1+self.b1
        self.a1=self.relu(self.z1)
        # print(self.a1)

        self.z2=self.a1@self.w2+self.b2
        self.a2=self.relu(self.z2)
        # print(self.a2)

        self.z3=self.a2@self.w3+self.b3
        self.y_pred=self.sigmoid(self.z3)

        return self.y_pred
    
    def backpropagation(self,x,y):
        m=y.shape[0]

        dz3=self.y_pred-y

        dw3=self.a2.T @ dz3/m
        db3=np.mean(dz3,axis=0,keepdims=True)


        da2=dz3 @ self.w3.T
        dz2=da2*self.relu_derivative(self.z2)
        dw2=self.a1.T @dz2/m
        db2=np.mean(dz2,axis=0,keepdims=True)

        da1=dz2 @ self.w2.T
        dz1=da1*self.relu_derivative(self.z1)
        dw1=x.T@dz1/m
        db1=np.mean(dz1,keepdims=True,axis=0)

        self.w1-=self.lr*dw1
        self.w2-=self.lr*dw2
        self.w3-=self.lr*dw3

        self.b1-=self.lr*db1
        self.b2-=self.lr*db2
        self.b3-=self.lr*db3
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






        
