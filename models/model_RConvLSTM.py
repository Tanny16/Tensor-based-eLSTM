# -*- coding: utf-8 -*-

from keras.layers import LSTM, Dense, Flatten, Dropout
from utils.RConvLSTM2D import RConvLSTM2D
from keras.models import Sequential


def get_model():
    model = Sequential()
    model.add(RConvLSTM2D(filters=5, kernel_size=(3, 3),
              input_shape=(None, 1, 11, 7), data_format="channels_first",
              padding='same', return_sequences=True))  # returns a sequence of vectors of dimension 32
    model.add(RConvLSTM2D(filters=5, kernel_size=(3, 3),
              input_shape=(None, 1, 11, 7), data_format="channels_first",
              padding='same'))  # return a single vector of dimension 32
    model.add(Flatten())
    model.add(Dropout(0.5))
    model.add(Dense(30, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    return model

def train(model, train_x, train_y, test_x, test_y):
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    model.fit(train_x, train_y,
              batch_size=1000, epochs=2, validation_data=(test_x, test_y))

def test_model(model, test_x, test_y):
    loss, acc = model.evaluate(test_x, test_y,
                               batch_size=1000)
    return acc


if __name__ == '__main__':
    pass
