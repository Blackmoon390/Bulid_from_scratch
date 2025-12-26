import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json


class single_weighted_perceptron():
    def __init__(self,lr=0.01,epoch=100000):

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
    

    
def confusion_matrix(y, y_pred):
    tp, tn, fp, fn = 0, 0, 0, 0

    for actual, pred in zip(y, y_pred):
        if actual == 1 and pred == 1:
            tp += 1
        elif actual == 0 and pred == 0:
            tn += 1
        elif actual == 0 and pred == 1:
            fp += 1
        elif actual == 1 and pred == 0:
            fn += 1

    return [[tn, fp],
            [fn, tp]]

