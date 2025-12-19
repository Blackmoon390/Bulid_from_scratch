import numpy as np #just used numpy for mean,random,array
import pandas as pd # for split  training set ,test set

class single_weighted_perceptron():
    def __init__(self,lr=0.01,epoch=1000000):

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

        itergap=self.epoch/10

        for _ in range(self.epoch):
            z=x@self.w+self.b
            ycap=self.sigmoid(z)

            dz = (self.w1 * y + self.w0 * (1 - y)) * (ycap - y)
            dw=x.T@dz/m
            db=np.mean(dz)

            if (_ % itergap == 0):
                 lossval = self.loss(ycap, y)
                 print(f"Iteration {_}, Loss: {lossval}")


            self.w-=self.lr*dw
            self.b-=self.lr*db
    
    def sigmoid(self,z):
        return 1/(1+np.exp(-z))
    
    
  
    def loss(self,ycap, y):
        eps = 1e-9
        return -np.mean(self.w1 * y * np.log(ycap + eps) + self.w0 * (1 - y) * np.log(1 - ycap + eps))
    
    def predict(self,x,threshold=0.5):
        z=x@self.w+self.b
        act=self.sigmoid(z)
        return (act >= threshold).astype(int)
        

        


 
data=pd.read_csv("dataset2.csv")

x=data.drop(columns=["motor"]).to_numpy()
y=data["motor"].to_numpy().reshape(-1,1).astype(float)
meanval=x.mean(axis=0)
std=x.std(axis=0)+1e-8
x=(x+meanval)/std
row,col=data.shape
x_train,x_test=x[:int(0.7*row),:],x[int(0.7*row):,:]
y_train,y_test=y[:int(0.7*row),:],y[int(0.7*row):,:]
print(x.shape,y.shape)
print(x_train.shape)


network=single_weighted_perceptron()
network.fit(x_train,y_train)
y_pred=network.predict(x_test)

print(np.mean(y_test == y_pred))

from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

sns.heatmap(confusion_matrix(y_test, y_pred),annot=True)
plt.show()






        
