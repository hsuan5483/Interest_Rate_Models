# -*- coding: utf-8 -*-
"""
@author: Pei Hsuan Hsu
"""

import os
from os.path import join
from scipy.optimize import minimize, LinearConstraint, Bounds
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %% folder path
path = os.getcwd()
src = join(path, "source")
out = join(path, "CIR_output (model sigma)")

# %% Read file
data = pd.read_excel(join(src, '市場殖利率資料20190630.xlsx'))
cols = data.columns[1:]

t_bill = pd.read_csv(join(src, 't-bill.csv'), index_col=0)
dr = t_bill.diff()

N = 250
his_sigma = np.std(dr).values[0]*np.sqrt(N)
his_sigma = his_sigma/np.sqrt(data['R(market)'][1])

# %% CIR Model
def CIR(x, r0, data):
    T = data['T(year)']
    gamma = np.sqrt(pow(x[0],2) + 2*pow(x[2],2))
    A = pow((2 * gamma * np.exp((x[0] + gamma) * T / 2)) / ((gamma + x[0]) * (np.exp(gamma * T) - 1) + 2 * gamma), 2 * x[0] * x[1] / x[2] ** 2)
    B = (2 * (np.exp(gamma * T) - 1)) / ((gamma + x[0]) * (np.exp(gamma * T) - 1) + 2 * gamma)
    R_CIR = -np.log(A) / T + B * r0 / T
    return A, B, R_CIR

def cir_error(x, r0, data):
    R_market = data['R(market)']
    _, _, R_CIR = CIR(x, r0, data)
    return sum(pow(R_market - R_CIR,2))

def RMSE(x, r0, data):
    R_market = data['R(market)']
    _, _, R_CIR = CIR(x, r0, data)
    return np.sqrt(pow(R_market - R_CIR,2))

#%% polt function
def plot_calibration(T, R_market, R_model, method, model_typ, sig_typ):
    
    figure, ax = plt.subplots(figsize=(6,4))
    ax.plot(T, R_market, label='R(market)')
    ax.plot(T, R_model, label='R('+model_typ+')')
    
    ax.set_title('Yield Curve Fitting Results ('+sig_typ+' sigma)')
    ax.set_xlabel('Time to Maturity')
    ax.set_ylabel('r')
    
    textstr = '\n'.join((
        r'='+method+'=',
        r'$a=%.6f$' % (x[0], ),
        r'$b=%.6f$' % (x[1], ),
        r'$\sigma=%.6f$' % (his_sigma, ),
        r'RMSE=%.4E' % (sum(RMSE(x, r0, mdata)), )))
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    
    ax.text(0.55, 0.45, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    
    plt.legend()
    plt.savefig(join(out, model_typ+' fitting result ('+sig_typ+' sigma - '+method+').png'))
    plt.show()

#%% calibration function
def CIR_calibration(mdata, r0, x0, method):
   # 限制式
   cons1 = LinearConstraint([[1,0,0],[0,1,0],[0,0,1]], [0.001, 0.001, 0.001], [15,15,1])
   
   cons2 = {'type':'ineq',
            'fun':lambda x: np.array([x[0]-0.001,
                                     15 - x[0],
                                     x[1]-0.001,
                                     15 - x[1],
                                     x[2]-0.001,
                                     1-x[2]])
           }
   
   if method == 'SLSQP' or method == 'COBYLA' or method == 'trust-constr':
       result = minimize(cir_error, x0, args=(r0, mdata), method=method, constraints=cons2)
       
   elif method == 'Nelder-Mead':
       result = minimize(cir_error, x0, args=(r0, mdata), method=method, tol = 10e-6, bounds=())
       
   else:
       result = minimize(cir_error, x0, args=(r0, mdata), method=method, constraints=cons1)
       
   x = result['x']
   rmse = RMSE(x, r0, mdata)
   
   print('====================')
   print('Optimization Results')
   print('====================')
   print('Model : CIR(model sigma)')
   print('Method :', method)
   print('r0 = %.6f' % r0)
   print('a = %.6f' % x[0])
   print('b = %.6f' % x[1])
   print('Historical Sigma = %.6f' % his_sigma)
   print('RMSE = %.4E' % sum(rmse))
   
   return x, rmse

#%% 參數估計
method = 'SLSQP'

mdata = data[1:-2].reset_index(drop=True)

# Set initial value
r0 = mdata['R(market)'][0]
a = 0.01
b = mdata[mdata['T(year)'] == 30].loc[:,'R(market)'].values[0]
x0 = [a, b, his_sigma]

### calibration results
x, rmse = CIR_calibration(mdata, r0, x0, method)
