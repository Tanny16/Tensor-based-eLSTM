# -*- coding: utf-8 -*-

acc = []

ID = []

with open("111.txt", "r") as f:
    for line in f.readlines():
        s_data = line.strip().split(":\t")
        acc.append((s_data[0], float(s_data[1])))
    result = sorted(acc, key=lambda x: x[1], reverse=True)
    print(result)

    for i in range(50):
        ID.append(result[0])

    # with open("ID_result.txt","a") as ff:
    #     for item in result:
    #         ff.writelines(item[0] + ":\t" + str(item[1]) + "\n")
