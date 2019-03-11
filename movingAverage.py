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
import matplotlib.pyplot as plt


w.start();

# 取数据的命令如何写可以用命令生成器来辅助完成
#wsd_data=w.wsi("T1903.CFE", "open,high,low,close,chg", "2018-11-12", "2019-02-11", "Fill=Previous","BarSize=5")  

wsd_data=w.wsd("T1803.CFE", "open,high,low,close,chg", "2017-11-12", "2018-02-11", "Fill=Previous")  

#演示如何将api返回的数据装入Pandas的DataFrame
fm=pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=wsd_data.Times)

fm=fm.T #将矩阵转置
fm['DATE'] = wsd_data.Times
#print(wsd_data.Times)
fm.set_index('DATE')

try:
    fm['CLOSE'] = fm['close']
    fm['OPEN'] = fm['open']
    fm['HIGH'] = fm['high']
    fm['LOW'] = fm['low']
    
except KeyError:
    print(1)


fm.dropna(inplace=True)  #清除null 
#print(fm)
fm.sort_values(by=['DATE'], inplace=True)



fm['CHG2'] = fm['CLOSE'].pct_change()

#fm.at[datetime.date(2018, 8, 12),'CHG2'] = 0

#print(fm[['CLOSE','CHG','CHG2']])

fm['复权因子'] = (fm['CHG2'] + 1).cumprod()

ma_short = 5
ma_long = 10

fm["ma_short"] = fm['CLOSE'].rolling(ma_short).mean()
fm["ma_long"] = fm['CLOSE'].rolling(ma_long).mean()

fm['ma_short'].fillna(value=fm['CLOSE'].expanding().mean(), inplace=True)
fm['ma_long'].fillna(value=fm['CLOSE'].expanding().mean(), inplace=True)

condition1 = (fm['ma_short'] > fm['ma_long'])
condition2 = (fm['ma_short'].shift(1) < fm['ma_long'].shift(1))

fm.loc[condition1 & condition2,'signal'] = 1  #买入信号

condition3 = (fm['ma_short'] < fm['ma_long'])
condition4 = (fm['ma_short'].shift(1) > fm['ma_long'].shift(1))

fm.loc[condition3 & condition4,'signal'] = 0    #卖出信号

#fm.drop(['ma_short','ma_long'],axis=1,inplace=True)

#fm['pos'] = fm['signal'].shift()  #信号是当天close买入 要第二天才可以买入 

fm['pos'] = fm['signal']

#涨跌停的时候不能买卖

limit_buy = fm['OPEN'] > fm['CLOSE'].shift(1) * 1.04  #涨停 4%

limit_sell = fm['OPEN'] < fm['CLOSE'].shift(1) * 0.96

fm.loc[limit_buy & (fm['pos'] == 1), 'pos'] = None

fm.loc[limit_sell & (fm['pos'] == 0), 'pos'] = None

fm['pos'].fillna(method='ffill',inplace=True)

fm['pos'].fillna(value=0,inplace=True) 

fm['equity_change'] = fm['CHG2'] * fm['pos']

fm['equity_curve'] = (fm['equity_change']+1).cumprod()

#fm = fm[['OPEN','CLOSE','HIGH','LOW','CHG2','pos','DATE']]

#print(fm.loc[fm['pos']==1])
#print(fm)
#print(fm['CLOSE'])


fm.reset_index(inplace=True,drop=True)

initial_money = 40000

slippage = 0

commission_rate = 0

tax_rate = 0

fm.at[0,'hold_num'] = 0
fm.at[0,'stock_value'] = 0
fm.at[0,'cash'] = initial_money
fm.at[0,'equity'] = initial_money
fm.at[0,'liability'] = 20000

#print(fm)
for i in range(1,fm.shape[0]):
    
    if fm.at[i,'pos'] != fm.at[i-1, 'pos']:
        number = fm.at[i-1,'equity'] * fm.at[i,'pos'] / fm.at[i,'OPEN'] #理论上今天持有的数量
        #print(fm.at[i-1,'equity'], fm.at[i,'pos'] ,fm.at[i,'OPEN'])
        number = int(number)
        
        if number > fm.at[i-1,'hold_num']:  # 买入
            
            buy = number - fm.at[i-1,'hold_num']
            
            buy_cash = buy * (fm.at[i,'OPEN'] + slippage)
            
            commission = buy_cash * commission_rate
            
            fm.at[i,'commission'] = commission
            
            fm.at[i,'hold_num'] = number
            
            fm.at[i,'cash'] = fm.at[i-1,'cash'] - buy_cash - commission
        
        else:
            sell = fm.at[i-1,'hold_num'] - number
            
            sell_cash = sell * (fm.at[i,'OPEN'] - slippage)
            
            commission = sell_cash * commission_rate
            
            fm.at[i,'commission'] = commission
        
            fm.at[i,'tax'] = sell_cash * tax_rate
            
            fm.at[i,'hold_num'] = number
            
            fm.at[i,'cash'] = fm.at[i-1,'cash'] + sell_cash - commission - sell_cash * tax_rate

    else:
                    
        fm.at[i,'hold_num'] = fm.at[i-1,'hold_num']
        
        fm.at[i,'cash'] = fm.at[i-1,'cash']

    fm.at[i,'stock_value'] = fm.at[i,'hold_num'] * fm.at[i,'CLOSE']

    fm.at[i,'equity'] = fm.at[i,'cash'] + fm.at[i,'stock_value']
    
        
        
        
    
print("ma_short ",ma_short," ,ma_long ",ma_long)
print(fm[['DATE','pos','equity','hold_num','OPEN','cash']])
#print(fm[['HIGH','LOW','OPEN','CLOSE','DATE']])

max_equity = fm['equity'].max()
print(max_equity)
min_equity = fm['equity'].min()

print('最大回撤率',str( (max_equity - min_equity)/max_equity * 100 ) + "%")

print('收益率',str(fm.iloc[-1]['equity'] / initial_money * 100 - 100) + "%")





plt.xlabel('date')
plt.ylabel('close price')
fm.CLOSE.plot()
fm.ma_short.plot()
fm.ma_long.plot()








