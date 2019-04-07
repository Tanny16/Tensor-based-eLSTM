# # encoding=utf-8
# import matplotlib.pyplot as plt
# from pylab import *                                 #支持中文
# mpl.rcParams['font.sans-serif'] = ['SimHei']
#
# names = ['3', '4', '5', '6', '7', '8', '9', '10']
# x = [3, 4, 5, 6, 7, 8, 9, 10]
# y = [0.59, 0.60, 0.57, 0.58, 0.59, 0.58, 0.61, 0.61]
# y1 = [0.61, 0.59, 0.59, 0.60, 0.60, 0.59, 0.61,  0.63]
# y2 = [0.64, 0.63, 0.64, 0.65, 0.65,  0.67, 0.65, 0.67]
# y3 = [0.65, 0.67, 0.68, 0.68, 0.68, 0.68, 0.67, 0.68]
# plt.plot(x, y, 'ro-')
# plt.plot(x, y1, 'bo-')
# plt.xlim(2, 11)  # 限定横轴的范围
# plt.ylim(0.4, 0.8)  # 限定纵轴的范围
# plt.plot(x, y, marker='o', ms=10, mec='r', mfc='w',label=u'ANN-S')
# plt.plot(x, y1, marker='+', ms=10, label=u'ANN-C')
# plt.plot(x, y2, marker='s', ms=10, label=u'LSTM')
# plt.plot(x, y3, marker='v', ms=10, label=u'R-LSTM')
# plt.legend()  # 让图例生效
# plt.xticks(x, names)
# plt.margins(0)
# plt.subplots_adjust(bottom=0.15)
# plt.xlabel(u"Time steps") #X轴标签
# plt.ylabel("Accuracy") #Y轴标签
# plt.savefig('test.png', format='png', bbox_inches='tight', transparent=True, dpi=1200)
#
# plt.show()

# import numpy as np
# from matplotlib import pyplot as plt
#
# plt.figure(figsize=(9, 6))
# n = 8
# X = np.arange(n) + 1
# # X是1,2,3,4,5,6,7,8,柱的个数
# # numpy.random.uniform(low=0.0, high=1.0, size=None), normal
# # uniform均匀分布的随机数，normal是正态分布的随机数，0.5-1均匀分布的数，一共有n个
# Y1 = np.random.uniform(0.5, 1.0, n)
# Y2 = np.random.uniform(0.5, 1.0, n)
# plt.bar(X, Y1, width=0.35, facecolor='lightskyblue', edgecolor='white')
# # width:柱的宽度
# plt.bar(X + 0.35, Y2, width=0.35, facecolor='yellowgreen', edgecolor='white')
# # 水平柱状图plt.barh，属性中宽度width变成了高度height
# # 打两组数据时用+
# # facecolor柱状图里填充的颜色
# # edgecolor是边框的颜色
# # 想把一组数据打到下边，在数据前使用负号
# # plt.bar(X, -Y2, width=width, facecolor='#ff9999', edgecolor='white')
# # 给图加text
# # for x, y in zip(X, Y1):
# #     plt.text(x + 0.3, y + 0.05, '%.2f' % y, ha='center', va='bottom')
# #
# # for x, y in zip(X, Y2):
# #     plt.text(x + 0.6, y + 0.05, '%.2f' % y, ha='center', va='bottom')
# plt.ylim(0, +1.25)
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

names = ['ANN-S', 'ANN-C', 'LSTM', 'R-LSTM']
size = 4
x = np.arange(size)
a = [0.66, 0.68, 0.71,0.74]
b = [0.57, 0.59, 0.64, 0.68]

total_width, n = 0.4, 2
width = total_width / n
x = x - (total_width - width) / 2

plt.bar(x - width, a,  width=width, facecolor='lightskyblue', linewidth=2, label='open')
plt.bar(x, b, width=width, facecolor='pink', linewidth=2, label='close')
plt.legend()
plt.ylim(0.4, 0.9)  # 限定纵轴的范围
plt.xticks(x, names)
plt.xlabel(u"Model") #X轴标签
plt.ylabel("Accuracy") #Y轴标签
# plt.grid(True, linestyle="-.", color="black", linewidth="1")
plt.savefig('test2.png', format='png', bbox_inches='tight', transparent=True, dpi=1200)
plt.show()
