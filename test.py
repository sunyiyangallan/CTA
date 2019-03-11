# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 11:27:58 2019

@author: Administrator
"""


returns = [1.0, 1.01, 1.05, 1.1, 1.11, 1.07, 1.03, 1.03, 1.01, 1.02, 1.04, 1.05, 1.07, 1.06, 1.05, 1.06, 1.07, 1.09, 1.12, 1.18, 1.15, 1.15, 1.18, 1.16, 1.19, 1.17, 1.17, 1.18, 1.19, 1.23, 1.24, 1.25, 1.24, 1.25, 1.24, 1.25, 1.24, 1.25, 1.24, 1.27, 1.23, 1.22, 1.18, 1.2, 1.22, 1.25, 1.25, 1.27, 1.26, 1.31, 1.32, 1.31, 1.33, 1.33, 1.36, 1.33, 1.35, 1.38, 1.4, 1.42, 1.45, 1.43, 1.46, 1.48, 1.52, 1.53, 1.52, 1.55, 1.54, 1.53, 1.55, 1.54, 1.52, 1.53, 1.53, 1.5, 1.45, 1.43, 1.42, 1.41, 1.43, 1.42, 1.45, 1.45, 1.49, 1.49, 1.51, 1.54, 1.53, 1.56, 1.52, 1.53, 1.58, 1.58, 1.58, 1.61, 1.63, 1.61, 1.59]

max_draw_down = 0
temp_max_value = 0
for i in range(1, len(returns)):
    temp_max_value = max(temp_max_value, returns[i-1])
    max_draw_down = min(max_draw_down, returns[i]/temp_max_value-1)
print(str(max_draw_down))


max_draw_down2=0
temp_max_value=0
for i in range(1,len(returns)):
    temp_max_value2 = min(returns[i:])
    
    max_draw_down2 = max(max_draw_down2,(returns[i]-temp_max_value2) / returns[i])
    
print(str(max_draw_down2))