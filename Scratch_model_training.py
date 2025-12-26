import Scratch_single_weighted_perceptron as ssp
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json

data=pd.read_csv("dataset2.csv")

x=data.drop(columns=["motor"]).to_numpy()
y=data["motor"].to_numpy().reshape(-1,1).astype(float)
meanval=x.mean(axis=0)
std=x.std(axis=0)+1e-8
x=(x+meanval)/std
row,col=data.shape
x_train,x_test=x[:int(0.7*row),:],x[int(0.7*row):,:]
y_train,y_test=y[:int(0.7*row),:],y[int(0.7*row):,:]

network=ssp.single_weighted_perceptron(epoch=1000000)
network.fit(x_train,y_train)

y_pred=network.predict(x_test)

cm=ssp.confusion_matrix(y_test,y_pred)

sns.heatmap(cm, annot=True, fmt=".0f", cmap="rocket",
            xticklabels=["0 (Negative)", "1 (Positive)"],
            yticklabels=["0 (Negative)", "1 (Positive)"])

plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.title("Confusion Matrix")

plt.tight_layout()                     
plt.savefig("confusion_matrix.png", dpi=300)
plt.show()

mean=x.mean(axis=0)
std=x.std(axis=0) + 1e-9

weights = {
    "type": "model",

    "mean": mean.tolist(),
    "std": std.tolist(),
    "w1":network.w.tolist(),
    "b1":network.b}

with open("model.json","w") as file:
    json.dump(weights,file)
