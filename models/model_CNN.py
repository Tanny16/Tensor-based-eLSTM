# -*- coding: utf-8 -*-

from keras.models import Sequential
from keras.layers import Dense, Dropout, Convolution2D, Activation, MaxPooling2D, Flatten, Reshape


def get_model():
    model = Sequential()
    model.add(Convolution2D(
        batch_input_shape=(None, 1, 5, 12),
        filters=32,
        kernel_size=3,
        strides=1,
        padding='same',
        data_format='channels_first',
    ))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(
        pool_size=2,
        strides=2,
        padding='same',
        data_format='channels_first',
    ))
    model.add(Convolution2D(64, 3, strides=1, padding='same', data_format='channels_first'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(2, 2, 'same', data_format='channels_first'))
    model.add(Flatten())
    model.add(Dense(100))
    model.add(Dropout(0.5))
    model.add(Dense(30, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
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
