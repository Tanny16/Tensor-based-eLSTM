# -*- coding: utf-8 -*-

import numpy as np

from Model import model_pre
from utils import GetData

print('Getting Data....')

ID = GetData.get_stock_ID('../Data/stock.txt')
ID.remove('600005')

x_train_list = []
y_train_list = []
x_test_list = []
y_test_list = []

i = 0

for stock in ID:
    i += 1
    print(str(i) + '\t' + stock)
    x_temp = GetData.get_data_quota(stock)
    x_train_list += x_temp[0:int(len(x_temp)*0.7)]
    x_test_list += x_temp[int(len(x_temp) * 0.7):]

for stock in ID:
    i += 1
    print(str(i) + '\t' + stock)
    x_temp, y_temp = GetData.get_data(stock)
    y_train_list += y_temp[0:int(len(y_temp)*0.7)]
    y_test_list += y_temp[int(len(y_temp) * 0.7):]


print('Training...')
x_train = np.array(x_train_list)
y_train = np.array(y_train_list)
x_test = np.array(x_test_list)
y_test = np.array(y_test_list)

print(x_train.shape)
print(x_test.shape)

model = model_pre.get_model()
model_pre.train(model, x_train, y_train)
acc = model_pre.test_model(model, x_test, y_test)

print(acc)
