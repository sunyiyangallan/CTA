# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 10:18:35 2019

@author: Administrator
"""

# -*- coding:utf-8 -*-
#Python 3.5.0
from WindPy import w
import pandas as pd
import datetime
w.start();

# 取数据的命令如何写可以用命令生成器来辅助完成
wsd_data=w.wsd("T1903.CFE", "open,high,low,close", "2018-04-10", "2019-01-02", usedf=True)
print(type(wsd_data))


#演示如何将api返回的数据装入Pandas的DataFrame
#fm=pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=wsd_data.Times)

#fm=fm.T #将矩阵转置
#fm['DATE'] = wsd_data.Times
#fm.set_index('DATE')

wsd_data.dropna(inplace=True)  #清楚null 
#print(fm)


