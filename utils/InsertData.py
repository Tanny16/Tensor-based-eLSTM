# -*- coding: utf-8 -*-

from pymongo import MongoClient


def get_post(item):
    post = {}
    post['Stkcd'] = item[0]
    post['Trddt'] = item[1]
    post['Opnprc'] = item[2]
    post['Hiprc'] = item[3]
    post['Loprc'] = item[4]
    post['Clsprc'] = item[5]
    post['Dnshrtrd'] = item[6]
    post['Dnvaltrd'] = item[7]
    post['Dsmvosd'] = item[8]
    post['Dsmvtll'] = item[9]
    post['Dretwd'] = item[10]
    post['Adjprcwd'] = item[12]
    return post


def get_data(path):
    x = []
    file_in = open(path)
    i = 0
    for line in file_in.readlines():
        if i > 0:
            s_data = line.strip().split('\t')  # strip()函数去除换行符，split()函数分割数据
            temp = []
            for i in range(len(s_data)):
                if i == 0 or i == 1:
                    print(s_data)
                    temp.append(s_data[i])
                elif i == 15:
                    pass
                else:
                    temp.append(float(s_data[i]))
            x.append(temp)
        i += 1
    return x


# if __name__ == '__main__':
#     x = get_data('rumors.csv')
#     print(x)


if __name__ == '__main__':
    client_new = MongoClient('localhost', 27017)
    db = client_new['stock']
    document = db['TRD_T']
    x = get_data('./../Data/TRD_Dalyr2.txt')
    i = 0
    for item in x:
        i += 1
        print(str(i) + ' :' + item[0])
        post = get_post(item)
        document.insert(post)
    client_new.close()
