# -*- coding: utf-8 -*-

from keras.models import Model
from keras.layers import Dense, Input


def get_model():

    data = Input(shape=(60,))
    encoded = Dense(50, activation='relu')(data)
    encoded = Dense(40, activation='relu')(encoded)
    encoder_output = Dense(40, activation='relu')(encoded)

    decoded = Dense(40, activation='relu')(encoder_output)
    decoded = Dense(50, activation='relu')(decoded)
    decoded = Dense(60, activation='relu')(decoded)

    autoencoder = Model(input=data, output=decoded)
    encoder = Model(input=data, output=encoder_output)

    return autoencoder, encoder


def train(model, train_x):
    model.compile(optimizer='adam', loss='mse')
    model.fit(train_x, train_x, epochs=20, batch_size=256, shuffle=True)


def test_model(model, test_x):
    result = model.predict(test_x)
    return result


if __name__ == '__main__':
    pass
