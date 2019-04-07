# -*- coding: utf-8 -*-

import numpy as np

from Model import model_RLSTM, model_ConvLSTM, model_RConvLSTM, model_LSTM
from utils import GetData


print('Getting Data....')

# ID = GetData.get_stock_ID('../Data/stock2.csv')
# ID = ['000063', '000527']
# ID = ['000001', '000002', '000027', '000063', '000069', '000157', '000338', '000402', '000527', '000562',
#       '000568', '000629', '000651', '000709', '000728', '000783', '000792', '000825', '000858', '000878',
#       '000898', '000983', '002024', '002142', '002202', '600000', '600005', '600009', '600010', '600011',
#       '600015', '600016', '600018', '600019', '600026', '600027', '600028', '600029', '600030', '600031',
#       '600036', '600048', '600050', '600089', '600104', '600150', '600177', '600188', '600309', '600320',
#       '600350', '600362', '600519', '600550', '600583', '600585', '600598', '600642', '600649', '600663',
#       '600688', '600717', '600795', '600808', '600832', '600837', '600875', '600900', '601006', '601009',
#       '601088', '601111', '601166', '601168', '601169', '601186', '601318', '601328', '601333', '601390',
#       '601398', '601600', '601601', '601628', '601666', '601699', '601727', '601766', '601808', '601857',
#       '601866', '601872', '601898', '601899', '601919', '601939', '601958', '601988', '601991', '601998']

ID = []
acc = []
with open("ID_result.txt", "r") as f:
    for line in f.readlines():
        s_data = line.strip().split(":\t")
        acc.append([s_data[0], float(s_data[1])])
    result = sorted(acc, key=lambda x: x[1], reverse=True)
    print(result)
    for i in range(1):
        ID.append(result[i][0])



i = 0
x_train_list = []
y_train_list = []
x_test_list = []
y_test_list = []
for stock in ID:
    i += 1
    print(str(i) + '\t' + stock)
    x_temp, y_temp = GetData.get_data_rumor_tensor(stock)
    x_train_list += x_temp[0:int(len(x_temp)*0.7)]
    y_train_list += y_temp[0:int(len(y_temp)*0.7)]
    x_test_list += x_temp[int(len(x_temp) * 0.7):]
    y_test_list += y_temp[int(len(y_temp) * 0.7):]

print('Training...')
print(np.array(x_train_list).shape)
x_train = np.array(x_train_list)
y_train = np.array(y_train_list)
x_test = np.array(x_test_list)
y_test = np.array(y_test_list)
s_train = np.array(x_train_list)
s_test = np.array(x_test_list)


# print('Training...')
# print(np.array(x_train_list).shape)
# x_train = np.array(x_train_list)
# y_train = np.array(y_train_list)
# x_test = np.array(x_test_list)
# y_test = np.array(y_test_list)
#
# s_train = np.array(x_train_list)
# s_test = np.array(x_test_list)

# model = model_CNN.get_model()
# model_CNN.train(model, x_train.reshape(-1, 1, 5, 12), y_train)
# acc = model_CNN.test_model(model, x_test.reshape(-1, 1, 5, 12), y_test)

# model = model_LSTM.get_model()
# model_LSTM.train(model, x_train, y_train)
# acc = model_LSTM.test_model(model, x_test, y_test)

# model = model_LSTM_variants.get_model()
# model_LSTM_variants.train(model, x_train, y_train)
# acc = model_LSTM_variants.test_model(model, x_test, y_test)

# model = model_RLSTM.get_model()
# model_RLSTM.train(model, x_train, y_train, x_test, y_test)
# acc = model_RLSTM.test_model(model, x_test, y_test)

# model = model_ConvLSTM.get_model()
# model_ConvLSTM.train(model, x_train, y_train, x_test, y_test)
# acc = model_ConvLSTM.test_model(model, x_test, y_test)

model = model_RConvLSTM.get_model()
model_RConvLSTM.train(model, x_train, y_train, x_test, y_test)
acc = model_RConvLSTM.test_model(model, x_test, y_test)

# model = model_FC.get_model()
# model_FC.train(model, x_train, y_train)
# acc = model_FC.test_model(model, x_test, y_test)

# autoencoder, encoder = AutoEncoder.get_model()
# AutoEncoder.train(autoencoder, x_train.reshape(-1, 60))
# res_train = AutoEncoder.test_model(encoder, x_train.reshape(-1, 60))

# autoencoder, encoder = AutoEncoder.get_model()
# AutoEncoder.train(autoencoder, x_test.reshape(-1, 60))
# res_test = AutoEncoder.test_model(encoder, x_test.reshape(-1, 60))

# model = model_pre.get_model()
# model_pre.train(model, res_train, y_train)
# acc = model_pre.test_model(model, res_test, y_test)

# model = model_Merge_LSTM.get_model()
# model_Merge_LSTM.train(model, x_train, s_train, y_train)
# acc = model_Merge_LSTM.test_model(model, x_test, s_test, y_test)

# model = model_Merge_FC.get_model()
# model_Merge_FC.train(model, x_train, s_train, y_train)
# acc = model_Merge_FC.test_model(model, x_test, s_test, y_test)

print(acc)
