# -*- coding: utf-8 -*-

import mongoengine as me

import copy
import utils.tensor_try as tensor_tucker
import numpy as np

from mongoengine.context_managers import switch_collection

me.connect('stock', host='127.0.0.1', port=27017)


class Stock(me.Document):
    _id = me.StringField(required=True)
    Stkcd = me.StringField(required=True)
    Trddt = me.StringField(required=True)
    Opnprc = me.FloatField(required=True)
    Hiprc = me.FloatField(required=True)
    Loprc = me.FloatField(required=True)
    Clsprc = me.FloatField(required=True)
    Dnshrtrd = me.FloatField(required=True)
    Dnvaltrd = me.FloatField(required=True)
    Dsmvosd = me.FloatField(required=True)
    Dsmvtll = me.FloatField(required=True)
    Dretwd = me.FloatField(required=True)
    Dretnd = me.FloatField(required=True)
    Adjprcwd = me.FloatField(required=True)
    Adjprcnd = me.FloatField(required=True)
    Markettype = me.FloatField(required=True)
    Trdsta = me.FloatField(required=True)


class Stock_Quota(me.Document):
    _id = me.StringField(required=True)
    Stkcd = me.StringField(required=True)
    Trddt = me.StringField(required=True)
    boll_up = me.FloatField(required=True)
    boll_down = me.FloatField(required=True)
    kdj_k = me.FloatField(required=True)
    kdj_d = me.FloatField(required=True)
    kdj_j = me.FloatField(required=True)
    macd_dif = me.FloatField(required=True)
    macd_dea = me.FloatField(required=True)
    macd_macd = me.FloatField(required=True)


class Rumor(me.Document):
    _id = me.StringField(required=True)
    Stkcd = me.StringField(required=True)
    QLabel = me.IntField(required=True)
    QNegtive = me.IntField(required=True)
    QPositive = me.IntField(required=True)
    Qdate = me.StringField(required=True)
    ALabel = me.IntField(required=True)
    ANegtive = me.IntField(required=True)
    APositive = me.IntField(required=True)
    Adate = me.StringField(required=True)


def form_data(data):
    zip_data = map(list, zip(*data))
    result = []
    for feature in list(zip_data):
        if max(feature) == min(feature):
            temp = feature
        else:
            temp = list(map(lambda a: (a-min(feature)) / (max(feature) - min(feature)), feature))
        result.append(temp)
    return list(map(list, zip(*result)))


def get_data_quota(ID):
    with switch_collection(Stock_Quota, 'TRD_quota') as StockS:
        data = StockS.objects(Stkcd=ID).all()

        data_form = form_data([[x['boll_up'], x['boll_down'], x['kdj_k'], x['kdj_d'], x['kdj_j'], x['macd_dif'],
                                x['macd_dea'], x['macd_macd']] for x in data])
        """
        data_form = form_data([[x['Opnprc'], x['Hiprc'], x['Loprc'], x['Clsprc']] for x in data])
        """
        x_train = []
        length = len(data_form)
        for i in range(length):
            if i < length - 5:
                temp_time = []
                for j in range(5):
                    temp_time.append(data_form[i + j])
                x_train.append(temp_time)
        return x_train


def get_data_rumor(ID):
    with switch_collection(Stock, 'TRD_T') as StockS:
        data = StockS.objects(Stkcd=ID).all()
        date = [x['Trddt'] for x in data]
        # data_temp = [[x['Opnprc'], x['Hiprc'], x['Loprc'], x['Clsprc'], x['Dnshrtrd'], x['Dnvaltrd'],
        #                         x['Dsmvosd'], x['Dsmvtll'], x['Dretwd'], x['Dretnd'], x['Adjprcwd'], x['Adjprcnd'],
        #                         x['Markettype'], x['Trdsta']] for x in data]
        data_temp = [[x['Opnprc'], x['Hiprc'], x['Loprc'], x['Clsprc'], x['Dnshrtrd'], x['Dnvaltrd'],
                      x['Dsmvosd'], x['Dsmvtll'], x['Dretwd'], x['Adjprcwd']] for x in data]

        data_form = form_data(data_temp)
        """
        data_form = form_data([[x['Opnprc'], x['Hiprc'], x['Loprc'], x['Clsprc']] for x in data])
        """
        x_train = []
        y_train = []
        length = len(data_form)
        with switch_collection(Rumor, 'TRD_rumor') as RumorS:
            rumor = RumorS.objects(Stkcd=ID).all()
            rumor_dict = {}
            for item in rumor:
                rumor_dict.setdefault(item['Qdate'].replace('/', '-'), [item['QLabel'], item['QPositive'],
                                                                        item['QNegtive'], item['ALabel'],
                                                                        item['APositive'], item['ANegtive']])
            for i in range(length):
                if i < length - 5:
                    temp_time = []
                    for j in range(5):
                        daily = copy.deepcopy(data_form[i + j])
                        if date[i + j] in rumor_dict:
                            if rumor_dict[date[i + j]][0]:
                                daily.extend(rumor_dict[date[i + j]])
                            else:
                                daily.extend(rumor_dict[date[i + j]])
                        else:
                            daily.append(0)
                            daily.append(0)
                            daily.append(0)
                            daily.append(0)
                            daily.append(0)
                            daily.append(0)
                        temp_time.append(daily)
                    x_train.append(temp_time)
                    # if (data_temp[i + 0][3] + data_temp[i + 1][3] + data_temp[i + 2][3] + data_temp[i + 3][3] + data_temp[i + 4][3] + data_temp[i + 5][3] + data_temp[i + 6][3] + data_temp[i + 7][3]+ data_temp[i + 8][3] + data_temp[i + 9][3] + data_temp[i + 10][3] + data_temp[i + 11][3] + data_temp[i + 12][3] + data_temp[i + 13][3] + data_temp[i + 14][3]) < \
                    #         (data_temp[i + 15][3] + data_temp[i + 16][3] + data_temp[i + 17][3] + data_temp[i + 18][3] + data_temp[i + 19][3] + data_temp[i + 20][3] + data_temp[i + 21][3] + data_temp[i + 22][3]+ data_temp[i + 23][3] + data_temp[i + 24][3] + data_temp[i + 25][3] + data_temp[i + 26][3] + data_temp[i + 27][3] + data_temp[i + 28][3] + data_temp[i + 29][3]):
                    if data_temp[i + 4][3] > data_temp[i + 5][3]:
                        y_train.append(0)
                    else:
                        y_train.append(1)
            return x_train, y_train


def get_data_rumor_tensor(ID):
    with switch_collection(Stock, 'TRD_T') as StockS:
        data = StockS.objects(Stkcd=ID).all()
        date = [x['Trddt'] for x in data]
        # data_temp = [[x['Opnprc'], x['Hiprc'], x['Loprc'], x['Clsprc'], x['Dnshrtrd'], x['Dnvaltrd'],
        #                         x['Dsmvosd'], x['Dsmvtll'], x['Dretwd'], x['Dretnd'], x['Adjprcwd'], x['Adjprcnd'],
        #                         x['Markettype'], x['Trdsta']] for x in data]
        data_temp = [[x['Opnprc'], x['Hiprc'], x['Loprc'], x['Clsprc'], x['Dnshrtrd'], x['Dnvaltrd'],
                      x['Dsmvosd'], x['Dsmvtll'], x['Dretwd'], x['Adjprcwd']] for x in data]

        data_form = form_data(data_temp)
        """
        data_form = form_data([[x['Opnprc'], x['Hiprc'], x['Loprc'], x['Clsprc']] for x in data])
        """
        x_train = []
        y_train = []
        length = len(data_form)
        with switch_collection(Rumor, 'TRD_rumor') as RumorS:
            rumor = RumorS.objects(Stkcd=ID).all()
            rumor_dict = {}
            for item in rumor:
                rumor_dict.setdefault(item['Qdate'].replace('/', '-'), [item['QLabel'], item['QPositive'],
                                                                        item['QNegtive'], item['ALabel'],
                                                                        item['APositive'], item['ANegtive']])
            for i in range(length):
                if i < length - 5:
                    temp_time = []
                    for k in range(5):
                        daily = copy.deepcopy(data_form[i + k])
                        if date[i + k] in rumor_dict:
                            rumor_list = rumor_dict[date[i + k]]
                        else:
                            rumor_list = np.zeros(6)
                        temp_tensor = tensor_tucker.get_matrix(daily, rumor_list)
                        temp_time.append([temp_tensor])
                    x_train.append(temp_time)
                    # if (data_temp[i + 0][3] + data_temp[i + 1][3] + data_temp[i + 2][3] + data_temp[i + 3][3] + data_temp[i + 4][3] + data_temp[i + 5][3] + data_temp[i + 6][3] + data_temp[i + 7][3]+ data_temp[i + 8][3] + data_temp[i + 9][3] + data_temp[i + 10][3] + data_temp[i + 11][3] + data_temp[i + 12][3] + data_temp[i + 13][3] + data_temp[i + 14][3]) < \
                    #         (data_temp[i + 15][3] + data_temp[i + 16][3] + data_temp[i + 17][3] + data_temp[i + 18][3] + data_temp[i + 19][3] + data_temp[i + 20][3] + data_temp[i + 21][3] + data_temp[i + 22][3]+ data_temp[i + 23][3] + data_temp[i + 24][3] + data_temp[i + 25][3] + data_temp[i + 26][3] + data_temp[i + 27][3] + data_temp[i + 28][3] + data_temp[i + 29][3]):
                    if data_temp[i + 4][3] > data_temp[i + 5][3]:
                        y_train.append(0)
                    else:
                        y_train.append(1)
            return x_train, y_train


def get_data(ID):
    with switch_collection(Stock, 'TRD_old') as StockS:
        data = StockS.objects(Stkcd=ID).all()
        data_temp = [[x['Opnprc'], x['Hiprc'], x['Loprc'], x['Clsprc'], x['Dnshrtrd'], x['Dnvaltrd'],
                                x['Dsmvosd'], x['Dsmvtll'], x['Dretwd'], x['Dretnd'], x['Adjprcwd'], x['Adjprcnd'],
                                x['Markettype'], x['Trdsta']] for x in data]
        data_form = form_data(data_temp)
        """
        data_form = form_data([[x['Opnprc'], x['Hiprc'], x['Loprc'], x['Clsprc']] for x in data])
        """
        x_train = []
        y_train = []
        length = len(data_form)
        for i in range(length):
            if i < length - 10:
                temp_time = []
                for j in range(5):
                    temp_time.append(data_form[i+j])
                x_train.append(temp_time)
                # if data_temp[i+5][3] < data_temp[i+5][0]:
                if (data_temp[i + 0][3] + data_temp[i + 1][3] + data_temp[i + 2][3] + data_temp[i + 3][3] +
                        data_temp[i + 4][3]) < (
                                data_temp[i + 5][3] + data_temp[i + 6][3] + data_temp[i + 7][3] + data_temp[i + 8][3] +
                    data_temp[i + 9][3]):
                    y_train.append(0)
                else:
                    y_train.append(1)
        return x_train, y_train


def get_stock_ID(filename):
    with open(filename, 'r') as file:
        stock_ID = []
        lines = file.readlines()
        for line in lines:
            s_data = line.strip().split(' ')
            stock_ID.append(s_data[0])
        return stock_ID


if __name__ == '__main__':
    print(get_stock_ID('stock.txt'))

