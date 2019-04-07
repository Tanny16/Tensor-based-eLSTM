# -*- coding: utf-8 -*-

from keras.models import Sequential
from keras.layers import Dense, Dropout, Reshape


def get_model():
    model = Sequential()
    model.add(Reshape((160,), input_shape=(8, 20)))
    # model.add(Dense(100, input_dim=60, activation='relu'))
    # model.add(Dropout(0.5))
    model.add(Dense(50, activation='relu'))
    model.add(Dropout(0.5))
    # model.add(Dense(30, activation='relu'))
    # model.add(Dropout(0.5))
    model.add(Dense(10, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    return model


def train(model, train_x, train_y):
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    model.fit(train_x, train_y,
              epochs=1,
              batch_size=64)


def test_model(model, test_x, test_y):
    loss, acc = model.evaluate(test_x, test_y, batch_size=64)
    return acc


if __name__ == '__main__':
    pass
