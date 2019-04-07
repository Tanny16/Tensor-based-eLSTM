# -*- coding: utf-8 -*-

from keras.models import Sequential
from keras.layers import Dense, Dropout, Reshape
from keras.utils import plot_model


def get_model():
    model = Sequential()
    # model.add(Reshape((40,), input_shape=(5, 8)))     # quota 数据需要
    model.add(Dense(20, input_dim=40, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    # model.add(Dense(1, input_dim=40, activation='sigmoid'))
    return model


def train(model, train_x, train_y):
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    model.fit(train_x, train_y,
              epochs=2,
              batch_size=64)


def test_model(model, test_x, test_y):
    loss, acc = model.evaluate(test_x, test_y, batch_size=64)
    return acc


if __name__ == '__main__':
    pass
