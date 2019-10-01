# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 17:08:21 2019

@author: us
"""

from matplotlib import pyplot as plt
from wordcloud import WordCloud
 

file =open('./result-jieba.txt','r')

string = file.read()

font =r'C:\Windows\Fonts\msyhbd.ttc'#设置字体
wc = WordCloud(font_path=font, #如果是中文必须要添加这个，否则会显示成框框
               background_color='black',
               width=1080,
               height=1080,
               ).generate(string)
wc.to_file('ss4.png') #保存图片
plt.imshow(wc)  #用plt显示图片
plt.axis('off') #不显示坐标轴
