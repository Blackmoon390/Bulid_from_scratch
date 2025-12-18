import numpy as np

class NeuralNetwork:
    def __init__(self, lr=0.1):
        self.lr = lr

        # Initialize weights
        self.W1 = np.random.randn(9, 16) * 0.01
        self.b1 = np.zeros((1, 16))

        self.W2 = np.random.randn(16, 8) * 0.01
        self.b2 = np.zeros((1, 8))

        self.W3 = np.random.randn(8, 1) * 0.01
        self.b3 = np.zeros((1, 1))

    # -------- activations --------
    def relu(self, z):
        return np.maximum(0, z)

    def relu_deriv(self, z):
        return (z > 0).astype(float)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    # -------- forward --------
    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self.relu(self.z1)

        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = self.relu(self.z2)

        self.z3 = self.a2 @ self.W3 + self.b3
        self.y_hat = self.sigmoid(self.z3)

        return self.y_hat

    # -------- loss (binary) --------
    def loss(self, y):
        eps = 1e-9
        return -np.mean(y*np.log(self.y_hat+eps) +
                        (1-y)*np.log(1-self.y_hat+eps))

    # -------- backward --------
    def backward(self, X, y):
        m = y.shape[0]

        # Output layer
        dz3 = self.y_hat - y
        dW3 = self.a2.T @ dz3 / m
        print(dW3.shape)
        db3 = np.mean(dz3, axis=0, keepdims=True)
        print(db3.shape)

        # Hidden layer 2
        da2 = dz3 @ self.W3.T
        dz2 = da2 * self.relu_deriv(self.z2)
        dW2 = self.a1.T @ dz2 / m
        db2 = np.mean(dz2, axis=0, keepdims=True)
        print(dW2.shape)
        print(db2.shape)


        # Hidden layer 1
        da1 = dz2 @ self.W2.T
        dz1 = da1 * self.relu_deriv(self.z1)
        dW1 = X.T @ dz1 / m
        db1 = np.mean(dz1, axis=0, keepdims=True)
        print(dW1.shape)
        print(db1.shape)

        # Update
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W3 -= self.lr * dW3
        self.b3 -= self.lr * db3

    # -------- train --------
    def train(self, X, y, epochs=1):
        for i in range(epochs):
            self.forward(X)
            loss = self.loss(y)
            self.backward(X, y)

            if i % 200 == 0:
                print(f"Epoch {i}, Loss: {loss:.4f}")

    # -------- predict --------
    def predict(self, X):
        y_hat = self.forward(X)
        return (y_hat > 0.5).astype(int)



# Dummy data
X = np.random.rand(200, 9)
y = (np.sum(X, axis=1) > 4.5).astype(int).reshape(-1, 1)


nn = NeuralNetwork(lr=0.1)
nn.train(X, y, epochs=1)

pred = nn.predict(X[:5])

