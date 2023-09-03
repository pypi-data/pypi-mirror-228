import os
import numpy as np
import joblib
import logging

class Perceptron:
    #eta - Learning rate
    def __init__(self, eta: float = None, epochs: int= None):
        self.weights = np.random.randn(3) * 1e-4 #small random weights
        training = (eta is not None) and (epochs is not None)
        if training:
            logging.info(f'intial weights before training: \n {self.weights}')
        self.eta = eta
        self.epochs = epochs
            
    
    def _z_outcome(self, inputs, weights):
        return np.dot(inputs, weights)
    
    def activation_function(self, z):
        return np.where(z > 0, 1, 0)
    
    def fit(self, X, y):
        self.X = X
        self.y = y
        
        X_with_bias = np.c_[self.X, -np.ones((len(self.X),1))] #c_ = for concatenation
        logging.info(f"X with bias: \n {X_with_bias}")
        
        for epoch in range(self.epochs):
            logging.info("--"*10)
            logging.info(f"for epoch >> {epoch}")
            logging.info("--"*10)
            
            Z = self._z_outcome(X_with_bias, self.weights)
            y_hat = self.activation_function(Z)
            logging.info(f"predicted value after forward pass: \n{y_hat}")
            
            self.error = self.y - y_hat
            logging.info(f"error: \n{self.error}")
            
            self.weights = self.weights + self.eta * np.dot(X_with_bias.T, self.error)
            logging.info(f"updated weights after epoch: {epoch+1}/{self.epochs}: \n{self.weights}")
            logging.info("##"*10)
    
    def predict(self, X):
        X_with_bias = np.c_[X, -np.ones((len(X),1))]
        Z = self._z_outcome(X_with_bias, self.weights)
        return self.activation_function(Z)
    
    def total_loss(self):
        total_loss = np.sum(self.error)
        logging.info(f"\ntotal loss: {total_loss}\n")
        return total_loss
    
    def _create_dir_return_path(self, model_dir, filename):
        os.makedirs(model_dir, exist_ok=True)
        return os.path.join(model_dir, filename)
            
    def save(self, filename, model_dir =None):
        if model_dir is not None:
            model_file_path = self._create_dir_return_path(model_dir, filename)
            joblib.dump(self, model_file_path)
        else:
            model_file_path = self._create_dir_return_path("model", filename)
            joblib.dump(self, model_file_path)
        logging.info(f"model is saved at {model_file_path}")
    
    def load(self, filepath):
        return joblib.load(filepath)