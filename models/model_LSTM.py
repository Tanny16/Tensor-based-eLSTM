# -*- coding: utf-8 -*-

from keras.layers import LSTM, Dense, Flatten, Dropout, GRU, ConvLSTM2D
from keras.models import Sequential


def get_model():
    model = Sequential()
    model.add(LSTM(32, return_sequences=True,
                   input_shape=(5, 16)))  # returns a sequence of vectors of dimension 32
    model.add(LSTM(32))  # return a single vector of dimension 32
    model.add(Dense(30, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    return model


def train(model, train_x, train_y):
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    model.fit(train_x, train_y,
              batch_size=128, epochs=10)


def test_model(model, test_x, test_y):
    loss, acc = model.evaluate(test_x, test_y,
                               batch_size=128)
    return acc


if __name__ == '__main__':
    pass
