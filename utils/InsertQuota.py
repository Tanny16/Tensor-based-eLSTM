# -*- coding: utf-8 -*-

from pymongo import MongoClient

from utils import test_plotboll, test_plotkdj, test_plotmacd


def get_post(item):
    post = {}
    post['Stkcd'] = item[0]
    post['Trddt'] = item[1]
    post['boll_up'] = item[2]
    post['boll_down'] = item[3]
    post['kdj_k'] = item[4]
    post['kdj_d'] = item[5]
    post['kdj_j'] = item[6]
    post['macd_dif'] = item[7]
    post['macd_dea'] = item[8]
    post['macd_macd'] = item[9]
    return post


def get_stock_ID(filename):
    with open(filename, 'r') as file:
        stock_ID = []
        lines = file.readlines()
        for line in lines:
            s_data = line.strip().split(' ')
            stock_ID.append(s_data[0])
        return stock_ID


def write_data(ID):
    client_new = MongoClient('localhost', 27017)
    db = client_new['Stock']
    document = db['TRD']
    data = document.find({"Stkcd": ID})
    with open('test.txt', 'w') as file:
        for item in data:
            file.writelines(str(item['Hiprc']) + "," + str(item['Loprc']) + ","
                            + str(item['Clsprc']) + "," + str(item['Opnprc']) + "\n")
    time_data = document.find({"Stkcd": ID})
    time = []
    for each in time_data:
        time.append(each['Trddt'])
    client_new.close()
    return time


def insert_data():
    client_new = MongoClient('localhost', 27017)
    db = client_new['Stock']
    document = db['TRD_quota']
    ID_list = get_stock_ID('../Prediction/stock.txt')
    ID_list.remove('600005')
    flag = 0
    for ID in ID_list:
        flag += 1
        time = write_data(ID)
        if len(time) == 0:
            continue
        up, down = test_plotboll.have_boll('test.txt')
        k, d, j = test_plotkdj.have_kdj('test.txt')
        dif, dea, macd = test_plotmacd.have_macd('test.txt')
        for i in range(len(up)):
            print(str(flag) + '\t' + ID + '\t' + str(i))
            item = [ID, time[i], up[i], down[i], k[i], d[i], j[i], dif[i], dea[i], macd[i]]
            post = get_post(item)
            document.insert(post)
    client_new.close()


if __name__ == '__main__':
    insert_data()