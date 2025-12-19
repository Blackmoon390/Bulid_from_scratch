import numpy as np #just used numpy for exponential function and max
import pandas as pd # for split  training set ,test set

class nn():
    def __init__(self,lr=0.001,epoch=3000):

        self.lr=lr
        self.epoch=epoch

    def fit(self,x,y):

        m,n=x.shape

        np.random.seed(42)
        self.w=np.random.randn(n,1)*0.01

        pos=np.sum(y==1)
        neg=np.sum(y==0)

        self.w1=m/(pos*2)
        self.w0=m/(neg*2)
        self.b=0.0

        for _ in range(self.epoch):
            z=x@self.w+self.b
            ycap=self.sigmoid(z)

            dz = (self.w1 * y + self.w0 * (1 - y)) * (ycap - y)
            dw=x.T@dz/m
            db=np.mean(dz)

            loss=
        
    
    
    def sigmoid(self,z):
        return 1/(1+np.exp(-z))
    
    
  
    def loss(self,ycap, y):
        eps = 1e-9
        -np.mean(self.w1 * y * np.log(ycap + eps) + self.w0 * (1 - y) * np.log(1 - ycap + eps))
        


 
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






        
