# -*- coding: utf-8 -*-

from pymongo import MongoClient


def get_post(item):
    post = {}
    post['Stkcd'] = item[0]
    post['QLabel'] = item[1]
    post['QNegtive'] = item[2]
    post['QPositive'] = item[3]
    post['Qdate'] = item[4]
    post['ALabel'] = item[5]
    post['ANegtive'] = item[6]
    post['APositive'] = item[7]
    post['Adate'] = item[8]
    return post


def get_data(path):
    x = []
    file_in = open(path)
    i = 0
    for line in file_in.readlines():
        if i > 0:
            s_data = line.strip().split(',')  # strip()函数去除换行符，split()函数分割数据
            temp = []
            for i in range(len(s_data)):
                if i == 0 or i == 4 or i == 8:
                    print(s_data)
                    temp.append(s_data[i])
                else:
                    temp.append(int(s_data[i]))
            x.append(temp)
        i += 1
    return x


# if __name__ == '__main__':
#     x = get_data('rumors.csv')
#     print(x)


if __name__ == '__main__':
    client_new = MongoClient('localhost', 27017)
    db = client_new['stock']
    document = db['TRD_rumor']
    x = get_data('./../Data/rumors.csv')
    i = 0
    for item in x:
        i += 1
        print(str(i) + ' :' + item[0])
        post = get_post(item)
        document.insert(post)
    client_new.close()
