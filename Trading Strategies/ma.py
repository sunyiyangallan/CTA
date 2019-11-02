# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 15:44:38 2019

@author: Administrator
"""

from WindPy import w
import pandas as pd
import datetime

def ma(ma_short,ma_long,fm):
    fm["ma_short"] = fm['CLOSE'].rolling(ma_short).mean()
    fm["ma_long"] = fm['CLOSE'].rolling(ma_long).mean()
    
    fm['ma_short'].fillna(value=fm['CLOSE'].expanding().mean(), inplace=True)
    fm['ma_long'].fillna(value=fm['CLOSE'].expanding().mean(), inplace=True)
    
    condition1 = (fm['ma_short'] > fm['ma_long'])
    condition2 = (fm['ma_short'].shift(1) < fm['ma_long'].shift(1))
    
    fm.loc[condition1 & condition2,'signal'] = 1  #买入信息
    
    condition3 = (fm['ma_short'] < fm['ma_long'])
    condition4 = (fm['ma_short'].shift(1) > fm['ma_long'].shift(1))
    
    fm.loc[condition3 & condition4,'signal'] = 0    #卖出信号
    
    fm.drop(['ma_short','ma_long'],axis=1,inplace=True)
    
    fm['pos'] = fm['signal'].shift()  #信号是当天close买入 要第二天才可以买入 
    
    
    
    #涨跌停的时候不能买卖
    
    limit_buy = fm['OPEN'] > fm['CLOSE'].shift(1) * 1.04  #涨停 4%
    
    limit_sell = fm['OPEN'] < fm['CLOSE'].shift(1) * 0.96
    
    fm.loc[limit_buy & (fm['pos'] == 1), 'pos'] = None
    
    fm.loc[limit_sell & (fm['pos'] == 0), 'pos'] = None
    
    fm['pos'].fillna(method='ffill',inplace=True)
    
    fm['pos'].fillna(value=0,inplace=True) #初始都设为0
    
    fm['equity_change'] = fm['CHG2'] * fm['pos']
    
    fm['equity_curve'] = (fm['equity_change']+1).cumprod()
    
    fm = fm[['OPEN','CLOSE','HIGH','LOW','CHG2','pos','DATE']]
    
    #print(fm.loc[fm['pos']==1])
    #print(fm)
    #print(fm['CLOSE'])
    
    
    fm.reset_index(inplace=True,drop=True)
    
    initial_money = 10000
    
    slippage = 1/100
    
    commission_rate = 0.1/10000
    
    tax_rate = 1/1000
    
    fm.at[0,'hold_num'] = 0
    fm.at[0,'stock_value'] = 0
    fm.at[0,'cash'] = initial_money
    fm.at[0,'equity'] = initial_money
    
    #print(fm)
    for i in range(1,fm.shape[0]):
        
        if fm.at[i,'pos'] != fm.at[i-1, 'pos']:
            number = fm.at[i-1,'equity'] * fm.at[i,'pos'] / fm.at[i,'OPEN'] #理论上今天持有的数量
            #print(fm.at[i-1,'equity'], fm.at[i,'pos'] ,fm.at[i,'OPEN'])
            number = int(number)
            
            if number > fm.at[i-1,'hold_num']:  # 买入
                buy = number - fm.at[i-1,'hold_num']
                
                buy_cash = buy * (fm.at[i-1,'OPEN'] + slippage)
                
                commission = buy_cash * commission_rate
                
                fm.at[i,'commission'] = commission
                
                fm.at[i,'hold_num'] = number
                
                fm.at[i,'cash'] = fm.at[i-1,'cash'] - buy_cash - commission
            
            else:
                sell = fm.at[i-1,'hold_num'] - number
                
                sell_cash = sell * (fm.at[i-1,'OPEN'] - slippage)
                
                commission = sell_cash * commission_rate
                
                fm.at[i,'commission'] = commission
            
                fm.at[i,'tax'] = sell_cash * tax_rate
                
                fm.at[i,'hold_num'] = number
                
                fm.at[i,'cash'] = fm.at[i-1,'cash'] + buy_cash - commission - sell_cash * tax_rate
    
        else:
                        
            fm.at[i,'hold_num'] = fm.at[i-1,'hold_num']
            
            fm.at[i,'cash'] = fm.at[i-1,'cash']
    
        fm.at[i,'stock_value'] = fm.at[i,'hold_num'] * fm.at[i,'CLOSE']
    
        fm.at[i,'equity'] = fm.at[i,'cash'] + fm.at[i,'stock_value']
        
            
            
            
        
    print("ma_short ",ma_short," ,ma_long ",ma_long)
    print(fm[['DATE','pos','equity','hold_num','CLOSE']])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




