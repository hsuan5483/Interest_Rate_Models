#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Pei-Hsuan Hsu
"""

import os
from os.path import join
import numpy as np
import pandas as pd
from scipy import exp, log, sqrt
from scipy.optimize import minimize
import matplotlib.pyplot as plt

path = os.getcwd()
src = join(path, "source")
out = join(path, "output")

'''
=============
Vesicek Model
=============
'''
# data
date = '20200401'
filename = date+' curve.xlsx'
data = pd.read_excel(join(src, filename))

# market data
T = data.iloc[1:-2,0]
R_market = data.iloc[1:-2,1]

# parameters
r0 = data.iloc[1,1]
a = 0.001
b = 0.001
sig = 0.001
x0 = [a, b, sig]
'''
x = [-0.000208371, 0.00629176, 0.00658325]
'''

def Vasicek(x, T):
    B = (1-exp(-x[0]*T))/x[0]
    A = exp((x[1]-0.5*pow(x[2]/x[0],2))*(B-T)-(0.25*pow(x[1]*B,2)/x[0]))
    R = (-log(A)+B*r0)/T
    return R

def error(x, T):
    R_V = Vasicek(x, T)
    return sum(pow(R_market-R_V,2))

result = minimize(error, x0, args=T, method='SLSQP')
x = result['x']

figure, ax = plt.subplots(figsize=(6,4))
ax.plot(T, R_market, label='R(market)')
ax.plot(T, Vasicek(x, T), label='R(Vasicek)')

ax.set_title('Yield Curve Fitting Results')
ax.set_xlabel('Maturity')
ax.set_ylabel('r')

plt.legend()
plt.savefig(join(out, date+'_fit.png'))
plt.show()

