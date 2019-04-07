# -*- coding: utf-8 -*-

from keras.models import Model
from keras.layers import Dense, Input, Dropout, Add, Reshape, Concatenate, LSTM


def get_model():
    input_1 = Input(shape=(5, 12))
    input_2 = Input(shape=(5, 6))

    x1 = LSTM(32, input_shape=(5, 12))(input_1)
    # x1 = LSTM(32)(x1)
    x1 = Dense(10, activation='relu')(x1)
    x1 = Dropout(0.5)(x1)
    x1 = Dense(5, activation='relu')(x1)

    x2 = LSTM(32, input_shape=(5, 6))(input_2)
    # x2 = LSTM(32)(x2)
    x2 = Dense(10, activation='relu')(x2)
    x2 = Dropout(0.5)(x2)
    x2 = Dense(5, activation='relu')(x2)

    added = Concatenate(axis=-1)([x1, x2])
    out = Dense(10, activation='relu')(added)
    out = Dropout(0.5)(out)
    out = Dense(1, activation='sigmoid')(added)

    model = Model(inputs=[input_1, input_2], outputs=out)

    return model


def train(model, train_x, train_s, train_y):
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    model.fit([train_x, train_s], train_y,
              batch_size=64, epochs=5)


def test_model(model, test_x, test_s, test_y):
    loss, acc = model.evaluate([test_x, test_s], test_y, batch_size=64)
    return acc


if __name__ == '__main__':
    pass
