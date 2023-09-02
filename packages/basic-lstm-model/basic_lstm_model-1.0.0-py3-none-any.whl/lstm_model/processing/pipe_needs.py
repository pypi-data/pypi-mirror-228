import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))

from keras.models import Sequential
from keras.layers import LSTM, Dense

import numpy as np

class ReestructuraLSM():
  '''The shape will go from (nrows, nfeatures) to (x, window_length, nfeatures), needed for the LSTM'''
  def __init__(self, ventana):
    self.ventana = ventana
  def fit(self, X, y=None):
    # We need this steep because of the compatibility with the Sklearn Pipeline.
    return self
  def transform(self, X):
    if (not isinstance(X, np.ndarray)):
      raise ValueError('Data should be a numpy array.')
    X = np.array([X[j-(self.ventana-1):j+1].tolist() for j in range(self.ventana-1,len(X)) ])
    return X

class ModeloLSM():
  '''Train LSTM, and predict'''
  def __init__(self, ventana,n_features,epochs):
    self.ventana = ventana
    self.n_features = n_features
    self.epochs = epochs
  def fit(self, X, y):
    self.modelo = Sequential()
    self.modelo.add(LSTM(50, activation='tanh', input_shape=(self.ventana, self.n_features)))
    self.modelo.add(Dense(1))
    self.modelo.compile(optimizer='adam', loss='mse')
    self.modelo.fit(X, y, epochs=self.epochs)
    return self
  def transform(self, X):
    return self.modelo.predict(X)

