import datetime
today = str(datetime.date.today())

import sys
sys.stdout = open(f'output_check_returns_{today}.txt', 'w')
sys.stderr = open(f'errors_check_returns_{today}.txt', 'w')

import math
import os.path
from os import path

import threading
import time

import pandas as pd
import numpy as np
import pickle
import glob
import os
import random

import datetime

'''

STOP_PERCENT = 0.25
MARGIN_PERCENT = 0.35
order_multiplier = 3.0


with open('margin-dict-maint.pkl','rb') as f:
  margin_dict_maint = pickle.load(f)

with open('margin-dict-init.pkl','rb') as f:
  margin_dict_init = pickle.load(f)




gap_up_df = pd.DataFrame()

for f in glob.glob('.\\*.csv'):
  gap_up_df = gap_up_df.append(pd.read_csv(f))

gap_up_df.drop_duplicates(subset='Symbol',inplace=True)

up_list = gap_up_df.Symbol.to_list()
random.shuffle(up_list)
up_list = list(set(up_list))

if 'GME' in up_list:
  up_list.remove('GME')
if 'GOOG' in up_list and 'GOOGL' in up_list:
  up_list.remove('GOOGL')


true_gap_down_df = pd.DataFrame()

true_gap_down_df = true_gap_down_df.append(pd.read_csv('..\\true_Gap_Down_May-04-2021.csv'))

true_gap_down_df.drop_duplicates(subset='Symbol',inplace=True)

true_gap_list = true_gap_down_df.Symbol.to_list()
random.shuffle(true_gap_list)
true_gap_list = list(set(true_gap_list))

if 'GME' in true_gap_list:
  true_gap_list.remove('GME')
if 'GOOG' in true_gap_list and 'GOOGL' in true_gap_list:
  true_gap_list.remove('GOOGL')


entered_tickers = ['CRK', 'GEVO', 'CBD', 'FCEL', 'DB', 'BFLY', 'SABR', 'CNHI', 'ACI', 'LAZR', 'ICLN', 'EH', 'VNE', 'BE', 'PLUG', 'RCM', 'BHC', 'MOS', 'BLNK', 'CSIQ', 'GRWG', 'RUN', 'VRNS', 'TPIC', 'CELH', 'EWT', 'DQ', 'TAN', 'SYNH', 'NET', 'CAR', 'SI', 'APPN', 'XPO', 'SEDG', 'ASML']

filtered_up_list = []
for ticker in up_list:
  if ticker in margin_dict_maint and ticker in margin_dict_init:
    if margin_dict_maint[ticker] < MARGIN_PERCENT and margin_dict_init[ticker] < MARGIN_PERCENT:
      filtered_up_list.append(ticker)



#print(filtered_up_list)
print(len(filtered_up_list))

print(len(set(filtered_up_list).intersection(true_gap_list)))



missing_tickers = set(filtered_up_list).intersection(true_gap_list)
for i in entered_tickers:
   if i in missing_tickers:
      missing_tickers.remove(i)

print(missing_tickers)
'''

def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')

download_path = get_download_path()


'''
# load margin data
with open('margin-dict-maint.pkl','rb') as f:
  margin_dict_maint = pickle.load(f)

with open('margin-dict-init.pkl','rb') as f:
  margin_dict_init = pickle.load(f)
'''

previous_day = pd.DataFrame()
for f in glob.glob(download_path + '\\previous_day\\*.csv'):
  previous_day = previous_day.append(pd.read_csv(f))

previous_day['close'] = previous_day['Close'].astype(float)
previous_day['open'] = previous_day['Open'].astype(float)


true_gap_up_df = pd.DataFrame()
for f in glob.glob(download_path + '\\actual_gap_up\\*.csv'):
  true_gap_up_df = true_gap_up_df.append(pd.read_csv(f))
true_gap_down_df = pd.DataFrame()
for f in glob.glob(download_path + '\\actual_gap_down\\*.csv'):
  true_gap_down_df = true_gap_down_df.append(pd.read_csv(f))

true_gap_up_df.drop_duplicates(subset='Symbol',inplace=True)

true_gap_up_list = true_gap_up_df.Symbol.to_list()
true_gap_up_list = list(set(true_gap_up_list))

true_gap_down_df.drop_duplicates(subset='Symbol',inplace=True)

true_gap_down_list = true_gap_down_df.Symbol.to_list()
true_gap_down_list = list(set(true_gap_down_list))





gap_up_df = pd.DataFrame()

for f in glob.glob(download_path + '\\Gap_Up_1%\\*.csv'):
  gap_up_df = gap_up_df.append(pd.read_csv(f))

gap_up_df.drop_duplicates(subset='Symbol',inplace=True)

up_list = gap_up_df.Symbol.to_list()
random.shuffle(up_list)
up_list = list(set(up_list))

if 'GME' in up_list:
  up_list.remove('GME')
if 'GOOG' in up_list and 'GOOGL' in up_list:
  up_list.remove('GOOGL')

previous_day_tickers = previous_day.Symbol.to_list()
for ticker in up_list:
  if ticker not in previous_day_tickers:
    up_list.remove(ticker)
    print('removing',ticker,'from up_list, since not in previous day list')
print('up tickers:', up_list)


gap_down_df = pd.DataFrame()

for f in glob.glob(download_path + '\\Gap_Down_1%\\*.csv'):
  gap_down_df = gap_down_df.append(pd.read_csv(f))

gap_down_df.drop_duplicates(subset='Symbol',inplace=True)

down_list = gap_down_df.Symbol.to_list()
random.shuffle(down_list)
down_list = list(set(down_list))

if 'GME' in down_list:
  down_list.remove('GME')
if 'GOOG' in down_list and 'GOOGL' in down_list:
  down_list.remove('GOOGL')
for ticker in down_list:
  if ticker not in previous_day_tickers:
    down_list.remove(ticker)
    print('removing',ticker,'from up_list, since not in previous day list')
print('down tickers:', down_list)







ordered_up = pd.read_csv('ordered_tickers_up.csv').values.tolist()
ordered_up = [x[0] for x in ordered_up]
print('ordered_up tickers', ordered_up)
ordered_down = pd.read_csv('ordered_tickers_down.csv').values.tolist()
ordered_down = [x[0] for x in ordered_down]
print('ordered_down tickers', ordered_down)

post_gap_up_df = pd.DataFrame()

for f in glob.glob(download_path + '\\actual_gap_up\\*.csv'):
  print(f)
  post_gap_up_df = post_gap_up_df.append(pd.read_csv(f))

post_gap_up_df.drop_duplicates(subset='Symbol',inplace=True)

post_up_list = post_gap_up_df.Symbol.to_list()
random.shuffle(post_up_list)
post_up_list = list(set(post_up_list))

if 'GME' in post_up_list:
  post_up_list.remove('GME')
if 'GOOG' in post_up_list and 'GOOGL' in post_up_list:
  post_up_list.remove('GOOGL')

for ticker in post_up_list:
  if ticker not in previous_day_tickers:
    post_up_list.remove(ticker)
    print('removing',ticker,'from post_up_list, since not in previous day list')


# remove tickers we already entered
filtered_post_up_list = [ticker for ticker in post_up_list if ticker not in ordered_up]

'''
gap_down_df = pd.DataFrame()

for f in glob.glob(download_path + '\\actual_gap_down\\*.csv'):
  print(f)
  gap_down_df = gap_down_df.append(pd.read_csv(f))

gap_down_df.drop_duplicates(subset='Symbol',inplace=True)

down_list = gap_down_df.Symbol.to_list()
random.shuffle(down_list)
down_list = list(set(down_list))

if 'GME' in down_list:
  down_list.remove('GME')
if 'GOOG' in down_list and 'GOOGL' in down_list:
  down_list.remove('GOOGL')
for ticker in down_list:
  if ticker not in previous_day_tickers:
    down_list.remove(ticker)
    print('removing',ticker,'from up_list, since not in previous day list')

# remove tickers we already entered
filtered_down_list = [ticker for ticker in down_list if ticker not in ordered_down]
print('new down tickers:', filtered_down_list)
'''






'''
# filter for margin requirements
tmp_filtered_list_up = []
for ticker in true_gap_up_list:
    if ticker in margin_dict_maint and ticker in margin_dict_init:
        if margin_dict_maint[ticker] < 0.35 and margin_dict_init[ticker] < 0.35:
            tmp_filtered_list_up.append(ticker)

three_requirements_list_up = list(set(up_list).intersection(tmp_filtered_list_up))
gapped_and_preopen_up = list(set(up_list).intersection(true_gap_up_list))


tmp_filtered_list_down = []
for ticker in true_gap_down_list:
    if ticker in margin_dict_maint and ticker in margin_dict_init:
        if margin_dict_maint[ticker] < 0.35 and margin_dict_init[ticker] < 0.35:
            tmp_filtered_list_down.append(ticker)

three_requirements_list_down = list(set(up_list).intersection(tmp_filtered_list_down))
gapped_and_preopen_down = list(set(up_list).intersection(true_gap_down_list))
'''
'''
entered_list = 'GEVO, CBD, TWO, FCEL, GOGL, ADT, CLNE, BLDP, CENX, LTHM, DNMR, BE, PLUG, AVYA, LESL, EXPI, PFE, TPIC, CF, UBER, LYFT, KLIC, CAH, RDFN, IIVI, XEC, NET, CTSH, GDDY, PTON, PENN, CVAC, FMC, ENPH, ZTS, ETSY, TXG, BDX, TWLO'.split(', ')
entered_list.sort()
three_requirements_list.sort()
print(entered_list)
print(three_requirements_list)
weird_list = entered_list
for i in weird_list:
  if i in three_requirements_list:
    weird_list.remove(i)
print(weird_list)
'''

preopen_up =  list(set(up_list).intersection(true_gap_up_list))
postopen_up =  list(set(filtered_post_up_list).intersection(true_gap_up_list))

returns_unfiltered_up = []
tickers_unfiltered_up = []

returns_preopen_up = []
tickers_preopen_up = []

returns_postopen_up = []
tickers_postopen_up = []

for ticker in true_gap_up_list:
  try:
    tmp_return = (previous_day[previous_day.Symbol == ticker].open.iloc[0] - previous_day[previous_day.Symbol == ticker].close.iloc[0]) / previous_day[previous_day.Symbol == ticker].open.iloc[0]
    returns_unfiltered_up.append(tmp_return)
    tickers_unfiltered_up.append(ticker)
  except:
    print(ticker, 'not in previous day')
    continue
for ticker in preopen_up:
  try:
    tmp_return = (previous_day[previous_day.Symbol == ticker].open.iloc[0] - previous_day[previous_day.Symbol == ticker].close.iloc[0]) / previous_day[previous_day.Symbol == ticker].open.iloc[0]
    returns_preopen_up.append(tmp_return)
    tickers_preopen_up.append(ticker)
  except:
    print(ticker, 'not in previous day')
    continue
for ticker in postopen_up:
  try:
    tmp_return = (previous_day[previous_day.Symbol == ticker].open.iloc[0] - previous_day[previous_day.Symbol == ticker].close.iloc[0]) / previous_day[previous_day.Symbol == ticker].open.iloc[0]
    returns_postopen_up.append(tmp_return)
    tickers_postopen_up.append(ticker)
  except:
    print(ticker, 'not in previous day')
    continue

print('GAP UP')
print(len(returns_unfiltered_up), 'gapped tickers on paper. Returns:',np.nanmean(returns_unfiltered_up))
print(len(returns_preopen_up), 'paper gapped tickers in preopen. Returns:', np.nanmean(returns_preopen_up))
print(len(returns_postopen_up), 'paper gapped tickers in postopen (only). Returns:', np.nanmean(returns_postopen_up))

true_up_returns = pd.DataFrame({'ticker' : tickers_unfiltered_up, 'return' : returns_unfiltered_up})
true_up_returns.to_csv('paper_returns_up.csv')
preopen_up_returns = pd.DataFrame({'ticker' : tickers_preopen_up, 'return' : returns_preopen_up})
preopen_up_returns.to_csv('preopen_returns_up.csv')
postopen_up_returns = pd.DataFrame({'ticker' : tickers_postopen_up, 'return' : returns_postopen_up})
postopen_up_returns.to_csv('postopen_returns_up.csv')

'''
returns_unfiltered = []
returns_filtered = []
returns_3req = []
returns_gp = []
for ticker in true_gap_down_list:
  try:
    tmp_return = -(previous_day[previous_day.Symbol == ticker].open.iloc[0] - previous_day[previous_day.Symbol == ticker].close.iloc[0]) / previous_day[previous_day.Symbol == ticker].open.iloc[0]
    returns_unfiltered.append(tmp_return)
  except:
    print(ticker, 'not in previous day')
    continue
for ticker in tmp_filtered_list_down:
  try:
    tmp_return = -(previous_day[previous_day.Symbol == ticker].open.iloc[0] - previous_day[previous_day.Symbol == ticker].close.iloc[0]) / previous_day[previous_day.Symbol == ticker].open.iloc[0]
    returns_filtered.append(tmp_return)
  except:
    print(ticker, 'not in previous day')
    continue
for ticker in three_requirements_list_down:
  try:
    tmp_return = -(previous_day[previous_day.Symbol == ticker].open.iloc[0] - previous_day[previous_day.Symbol == ticker].close.iloc[0]) / previous_day[previous_day.Symbol == ticker].open.iloc[0]
    returns_3req.append(tmp_return)
  except:
    print(ticker, 'not in previous day')
    continue
for ticker in gapped_and_preopen_down:
  try:
    tmp_return = -(previous_day[previous_day.Symbol == ticker].open.iloc[0] - previous_day[previous_day.Symbol == ticker].close.iloc[0]) / previous_day[previous_day.Symbol == ticker].open.iloc[0]
    returns_gp.append(tmp_return)
  except:
    print(ticker, 'not in previous day')
    continue

print('GAP DOWN')
print(len(returns_unfiltered), 'gapped tickers. Of which', np.count_nonzero(np.isnan(returns_unfiltered)), 'failed to process in returns below')
print(len(returns_filtered), 'gapped tickers with margin requirement. Of which', np.count_nonzero(np.isnan(returns_filtered)), 'failed to process')
print(len(returns_3req), 'gapped tickers with margin requirement and on the preopen list. Of which', np.count_nonzero(np.isnan(returns_filtered)), 'failed to process')
print(len(returns_gp), 'gapped tickers on the preopen list. Of which', np.count_nonzero(np.isnan(returns_filtered)), 'failed to process')
print(np.nanmean(returns_unfiltered))
print(np.nanmean(returns_filtered))
print(np.nanmean(returns_3req))
print(np.nanmean(returns_gp))

'''

sys.stdout.close()
sys.stderr.close()