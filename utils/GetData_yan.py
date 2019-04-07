# -*- coding: utf-8 -*-

import mongoengine as me
import codecs
import copy
import pandas as pd
import numpy as np
import os

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
    Adjprcwd = me.FloatField(required=True)


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


def get_data_emotion(ID):
    with switch_collection(Stock, 'TRD_old') as StockS:
        data = StockS.objects(Stkcd=ID).all()
        date = [x['Trddt'] for x in data]
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
        with switch_collection(Rumor, 'TRD_rumor') as RumorS:
            rumor = RumorS.objects(Stkcd=ID).all()
            rumor_dict = {}
            for item in rumor:
                rumor_dict.setdefault(item['Qdate'].replace('/', '-'), item['QLabel'])
            for i in range(length):
                if i < length - 5:
                    temp_time = []
                    for j in range(5):
                        daily = copy.deepcopy(data_form[i + j])
                        if date[i + j] in rumor_dict:
                            print('11111111')
                            if rumor_dict[date[i + j]]:
                                daily.append(1)
                            else:
                                daily.append(-1)
                        else:
                            daily.append(0)
                        temp_time.append(daily)
                    x_train.append(temp_time)
                    if data_temp[i + 5][3] < data_temp[i + 5][0]:
                        y_train.append(0)
                    else:
                        y_train.append(1)
            return x_train, y_train


def get_data(ID):
    with switch_collection(Stock, 'TRD_T') as StockS:
        data = StockS.objects(Stkcd=ID).all()
        date = [x['Trddt'] for x in data]
        data_temp = [[x['Opnprc'], x['Hiprc'], x['Loprc'], x['Clsprc'], x['Dnshrtrd'], x['Dnvaltrd'],
                                x['Dsmvosd'], x['Dsmvtll'], x['Dretwd'], x['Adjprcwd']] for x in data]
        data_form = form_data(data_temp)
        """
        data_form = form_data([[x['Opnprc'], x['Hiprc'], x['Loprc'], x['Clsprc']] for x in data])
        """
        x_train = []
        y_train = []
        length = len(data_form)
        emotion_dict = get_stock_emotion(ID)
        for i in range(length):
            if i < length - 5:
                temp_time = []
                for j in range(5):
                    daily = copy.deepcopy(data_form[i + j])
                    if date[i + j] in emotion_dict:
                        if emotion_dict[date[i + j]]:
                            daily.append(1)
                        else:
                            daily.append(-1)
                    else:
                        daily.append(0)
                    temp_time.append(daily)
                x_train.append(temp_time)
                if data_temp[i+5][3] < data_temp[i+4][3]:
                    y_train.append(0)
                else:
                    y_train.append(1)
        return x_train, y_train, date


def get_stock_emotion(ID):
    filename = '../Data/hushen300_tag/' + ID + '.xlsx'
    if not os.path.exists(filename):
        return {}
    e_data = pd.read_excel(filename, index_col=None, na_values=['NA'], parse_cols="B, F")
    e_data = np.array(e_data)
    emotion_dict = {}
    for item in e_data:
        emotion_dict.setdefault(str(item[0])[0:10], int(item[1]))
    return emotion_dict


def get_stock_ID(filename):
    with codecs.open(filename, 'r', 'utf-8') as file:
        stock_ID = []
        lines = file.readlines()
        for line in lines:
            s_data = line.strip().split(',')
            stock_ID.append(s_data[0])
        return stock_ID


if __name__ == '__main__':
    # print(get_stock_ID('../Data/id_name.csv'))
    print(get_stock_emotion('000001'))
