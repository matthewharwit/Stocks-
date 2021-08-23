import sys
sys.stdout = open('output_log_postopen.txt', 'w')
sys.stderr = open('error_log_postopen.txt', 'w')

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from ibapi import wrapper
from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *

from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *

from ibapi.order_condition import * # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
from ibapi.order_state import * # @UnusedWildImport

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



STOP_PERCENT = 0.15 
MARGIN_PERCENT = 0.35
order_multiplier = 2.0 #only used in post open for intended quantity. Up_quantity used in placing orders. 

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

previous_day = pd.DataFrame()
for f in glob.glob(download_path + '\\previous_day\\*.csv'):
  previous_day = previous_day.append(pd.read_csv(f))

previous_day['close'] = previous_day['Close'].astype(float)

#with open('schwab_list.pkl','rb') as f:
#  tickers_schwab = pickle.load(f)

'''
with open('margin-dict-maint.pkl','rb') as f:
  margin_dict_maint = pickle.load(f)

with open('margin-dict-init.pkl','rb') as f:
  margin_dict_init = pickle.load(f)
'''

import socket, time
class IBApi(EWrapper, EClient):
    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.got_balance_flag = 0
        self.original_stored_balance = 0
        self.marginchange = 0
    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)
    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)
    
    @iswrapper
    # ! [openorder]
    def openOrder(self, orderId: OrderId, contract: Contract, order: Order,
                  orderState: OrderState):
        super().openOrder(orderId, contract, order, orderState)
        self.marginchange = orderState.maintMarginChange
        '''
        print("OpenOrder. PermId: ", order.permId, "ClientId:", order.clientId, " OrderId:", orderId, 
              "Account:", order.account, "Symbol:", contract.symbol, "SecType:", contract.secType,
              "Exchange:", contract.exchange, "Action:", order.action, "OrderType:", order.orderType,
              "TotalQty:", order.totalQuantity, "CashQty:", order.cashQty, 
              "LmtPrice:", order.lmtPrice, "AuxPrice:", order.auxPrice, "Status:", orderState.status)
        '''
        order.contract = contract

    @iswrapper
    def nextValidId(self, orderId:int):
        print("setting nextorderid: %d", orderId)
        self.nextorderid = orderId
        # here is where you start using api
        self.reqAccountSummary(9002, "All", "$LEDGER")

    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

    @iswrapper
    def accountSummary(self, reqId:int, account:str, tag:str, value:str, currency:str):
        if (self.got_balance_flag == 0) & (tag == "CashBalance"):
            self.got_balance_flag = 1
            self.original_stored_balance = value
            #print("Acct Summary. ReqId:" , reqId , "Acct:", account, 
            #    "Tag: ", tag, "Value:", value, "Currency:", currency)

    @iswrapper
    def accountSummaryEnd(self, reqId:int):
        print("AccountSummaryEnd. Req Id: ", reqId)

    def _socketShutdown(self):
        self.conn.lock.acquire()
        try:
            if self.conn.socket is not None:
                self.conn.socket.shutdown(socket.SHUT_WR)
        finally:
            self.conn.lock.release()

def stock_order(symbol):
	contract = Contract()
	contract.symbol = symbol
	contract.secType = 'STK'
	contract.exchange = 'SMART'
	contract.PrimaryExch = "ISLAND"
	contract.currency = 'USD'
	return contract

def run_loop():
	app.run()

app = IBApi()
app.connect('127.0.0.1', 7496, 321)

api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(5)
original_balance = float(app.original_stored_balance)


ordered_up = pd.read_csv('ordered_tickers_up.csv').values.tolist()
ordered_up = [x[0] for x in ordered_up]
print('ordered_up tickers', ordered_up)
ordered_down = pd.read_csv('ordered_tickers_down.csv').values.tolist()
ordered_down = [x[0] for x in ordered_down]
print('ordered_down tickers', ordered_down)


#change made - added ETF_list
ETF_list = ['SIL', 'VIXY', 'TRHC', 'GSAH', 'ARCO', 'DHT', 'NUGT', 'PRPB', 'AFIN', 'JUSHF', 'CPUH/U', 'VXX', 'LIT', 'GSG', 'JWS', 'WBAI', 'WCLD', 'PLL', 'RWT', 'DHC', 'EWW', 'BPFH', 'RPV', 'AAC/U', 'KAHC/U', 'JWSM/U', 'TBT', 'EVRI', 'BLOK', 'REM', 'BPMP', 'PLYA', 'JPST', 'NBLX', 'SDC', 'GEM', 'WPF', 'XHB', 'PFFD', 'EWA', 'STPK', 'ASZ/U', 'FNGU', 'DBC', 'VRP', 'LMNX', 'IXC', 'WDR', 'FALN', 'EWH', 'SH', 'VGLT', 'PLT', 'RSX', 'IPOF', 'UVXY', 'USA', 'SQQQ', 'CVII/U', 'FPRX', 'PAND', 'ILF', 'GAB', 'EWL', 'FTSL', 'TNA', 'PBUS', 'BDJ', 'GNMK', 'PGF', 'TECL', 'CEQP', 'SPXL', 'EMLP', 'IPOE', 'IYF', 'XME', 'MJ', 'PMT', 'BSCL', 'UPRO', 'YQ', 'HOME', 'ESGE', 'AMJ', 'CXP', 'PEJ', 'FEZ', 'PSLV', 'FAS', 'PAVE', 'ESRT', 'KBWB', 'ABR', 'ANGL', 'ARI', 'TWO', 'TLND', 'QYLD', 'GLUU', 'ITB', 'PDM', 'PZA', 'FLRN', 'EGOV', 'CTRE', 'BDN', 'SGOL', 'BTRS', 'SPIP', 'FOCS', 'SHYG', 'IVOL', 'RPAI', 'FSK', 'SPSM', 'XLRE', 'IGLB', 'PBW', 'EPRT', 'BOTZ', 'KRE', 'ASHR', 'SBGI', 'SPTI', 'EWG', 'PS', 'EXG', 'RLJ', 'KBE', 'REET', 'SSO', 'SPHD', 'CTB', 'PCY', 'CIM', 'AIA', 'PSEC', 'SPTL', 'AEL', 'RDVY', 'TIGR', 'IQLT', 'SCHR', 'QCLN', 'FRHC', 'SPYD', 'DNP', 'GSY', 'SPTS', 'OFC', 'LXP', 'PRG', 'CLNY', 'CMD', 'QTEC', 'PCI', 'HMSY', 'FSKR', 'HYD', 'EMLC', 'APAM', 'TAN', 'PEB', 'SPMB', 'XOP', 'EWU', 'CIBR', 'ARKQ', 'STAY', 'EQC', 'APLE', 'WRI', 'USO', 'LGF/B', 'LGF/A', 'CNNE', 'SOXL', 'IDV', 'EWC', 'SRLN', 'ACWX', 'SPMD', 'DBEF', 'SBRA', 'QLD', 'DOC', 'FXI', 'KWEB', 'FNDE', 'QTS', 'SJNK', 'GLDM', 'HASI', 'CEF', 'SLYV', 'AB', 'ARKF', 'PDBC', 'HPP', 'FNB', 'VPL', 'HR', 'AMLP', 'JAMF', 'JETS', 'ACWV', 'NEA', 'IYR', 'MTG', 'TGNA', 'VDE', 'NRZ', 'NEAR', 'BXMT', 'PRSP', 'GUNR', 'XSOE', 'ISTB', 'SMH', 'FTSM', 'IGV', 'EZU', 'FIXD', 'SCHH', 'ICSH', 'ICLN', 'PSTH', 'INDA', 'GDXJ', 'VCLT', 'ORCC', 'SPAB', 'VLY', 'CLGX', 'SKYY', 'EWZ', 'FR', 'BKLN', 'SPIB', 'USIG', 'SCHP', 'FLOT', 'SPEM', 'FNDF', 'FPE', 'SOXX', 'HTA', 'TMX', 'EWT', 'HYLB', 'CWB', 'REXR', 'IYW', 'MCHI', 'AAXJ', 'PGX', 'AIRC', 'XLB', 'GWPH', 'LMBS', 'CCIV', 'STWD', 'ARKW', 'FLIR', 'VGIT', 'VFH', 'TCF', 'SPSB', 'USHY', 'SPLV', 'EWY', 'SCHO', 'NNN', 'XBI', 'SPLG', 'FRT', 'BPY', 'VSS', 'JEF', 'BBJP', 'SCHZ', 'IPHI', 'RP', 'IUSV', 'IJS', 'SCHE', 'SCHV', 'SPYG', 'VNO', 'TQQQ', 'EFAV', 'SPDW', 'PRAH', 'JNK', 'ARKG', 'SPYV', 'EFG', 'VGSH', 'IBB', 'EFV', 'FVD', 'XLP', 'IGIB', 'IEI', 'IUSB', 'VTEB', 'XLU', 'SCZ', 'VTIP', 'GSLC', 'IWO', 'BIL', 'IWS', 'QUAL', 'XLC', 'EWJ', 'IEF', 'VMBS', 'MTUM', 'VLUE', 'GOVT', 'IWP', 'MINT', 'TLT', 'LBTYK', 'LBTYA', 'ESGU', 'BIV', 'ACWI', 'SLV', 'XLI', 'GDX', 'SCHA', 'NWS', 'ASX', 'VAR', 'SHV', 'MAA', 'IWN', 'DGRO', 'DVY', 'PFF', 'SDY', 'SUZ', 'EMB', 'XLY', 'VT', 'SCHB', 'SHY', 'RF', 'SCHD', 'VGK', 'MDY', 'EFX', 'MUB', 'IVE', 'GMAB', 'NTRS', 'HYG', 'IGSB', 'GSX', 'ARKK', 'RSP', 'WORK', 'NDAQ', 'BDRFY', 'XLV', 'SCHF', 'TIP', 'CBRE', 'MBB', 'IXUS', 'IWB', 'IWR', 'SCHX', 'DIA', 'USMV', 'IAU', 'EDU', 'EEM', 'DFS', 'LBRDK', 'IVW', 'BSV', 'VYM', 'CCL', 'Z', 'BF/B', 'ALXN', 'ITOT', 'PRU', 'XLK', 'VCSH', 'XLF', 'VGT', 'MFC', 'VCIT', 'VXUS', 'VBR', 'LQD', 'DISCK', 'RELX', 'DOW', 'IWD', 'VEU', 'VIG', 'PBR/A', 'EFA', 'LNSTY', 'IJH', 'IWF', 'IJR', 'BND', 'IWM', 'IEMG', 'AGG', 'IEFA', 'GLAXF', 'VEA', 'ENLAY', 'VXF', 'VWO', 'VTV', 'VB', 'VO', 'VUG', 'QQQ', 'RDS/B', 'RDS/A', 'IVV', 'SPY', 'BRK/B', 'VOO', 'VTI']

gap_up_df = pd.DataFrame()

for f in glob.glob(download_path + '\\actual_gap_up\\*.csv'):
  print(f)
  gap_up_df = gap_up_df.append(pd.read_csv(f))

gap_up_df.drop_duplicates(subset='Symbol',inplace=True)

up_list = gap_up_df.Symbol.to_list()
random.shuffle(up_list)
up_list = list(set(up_list))

#change made - added filter below  
up_list = [x for x in up_list if x not in ETF_list]

if 'GME' in up_list:
  up_list.remove('GME')
if 'LWLG' in up_list:
  up_list.remove('LWLG')
if 'GOOG' in up_list and 'GOOGL' in up_list:
  up_list.remove('GOOGL')
if 'HOOD' in up_list:
  up_list.remove('HOOD')
  

previous_day_tickers = previous_day.Symbol.to_list()
for ticker in up_list:
  if ticker not in previous_day_tickers:
    up_list.remove(ticker)
    print('removing',ticker,'from up_list, since not in previous day list')


# remove tickers we already entered
filtered_up_list = [ticker for ticker in up_list if ticker not in ordered_up]
print('new up tickers:', filtered_up_list)

#gap_down_df = pd.DataFrame()

# for f in glob.glob(download_path + '\\actual_gap_down\\*.csv'):
#   print(f)
#   gap_down_df = gap_down_df.append(pd.read_csv(f))

# gap_down_df.drop_duplicates(subset='Symbol',inplace=True)

# down_list = gap_down_df.Symbol.to_list()
# random.shuffle(down_list)
# down_list = list(set(down_list))

# if 'GME' in down_list:
#   down_list.remove('GME')
# if 'LWLG' in down_list:
#   down_list.remove('LWLG')
# if 'GOOG' in down_list and 'GOOGL' in down_list:
#   down_list.remove('GOOGL')
# for ticker in down_list:
#   if ticker not in previous_day_tickers:
#     down_list.remove(ticker)
#     print('removing',ticker,'from up_list, since not in previous day list')

# # remove tickers we already entered
# filtered_down_list = [ticker for ticker in down_list if ticker not in ordered_down]
# print('new down tickers:', filtered_down_list)



up_quantity = pd.read_csv('up_quantity.csv').values.tolist()
up_quantity = [x[0] for x in up_quantity][0]
print('up_quantity')
down_quantity = pd.read_csv('down_quantity.csv').values.tolist()
down_quantity = [x[0] for x in down_quantity][0]
print('down_quantity')


'''
filtered_up_list = []
for ticker in up_list:
  if ticker in margin_dict_maint and ticker in margin_dict_init:
    if margin_dict_maint[ticker] < MARGIN_PERCENT and margin_dict_init[ticker] < MARGIN_PERCENT:
      filtered_up_list.append(ticker)
'''
#filtered_up_list = up_list

up_list_biggap = list(set(gap_up_df[gap_up_df['% Gap'] > 3.5].Symbol.to_list()))

big_and_filtered = []
for ticker in filtered_up_list:
  if ticker in up_list_biggap:
    big_and_filtered.append(ticker)
total_big_filtered = len(up_list_biggap) #big_and_filtered

#Preopen this is set to 16, so assuming 60% or less get filled from the original list, then multiply post open multiplier by 2.
#order multiplier not used in postopen in actually placing orders, instead uses up_quantity, thus I multiplied that by 2. 
if total_big_filtered < 16:     
    up_quantity = up_quantity *2

    

#Place orders
delay_counter = 0
for ticker in filtered_up_list:
      if delay_counter == 45:
        delay_counter = 0
        time.sleep(1)
      delay_counter += 3
      try:
        print('ticker:', ticker)
        #print('maint margin:', margin_dict_maint[ticker], 'init margin:',margin_dict_init[ticker])
        #print('API price, open:',open_dict[ticker], 'current:', current_dict[ticker]) #, 'previous close:', previous_day[(previous_day['Unnamed: 1'] == ticker) & (previous_day['Unnamed: 0'] == 'Close')][day_index].iloc[0])
        print('previous close:', previous_day[previous_day['Symbol'] == ticker].close.iloc[0])
        print('intended quantity:', int( (order_multiplier * original_balance / total_big_filtered) / (previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * 1.025) ))
        print('intended stop price:', str(round(previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * (1.025 + STOP_PERCENT),2)))
        # INITIAL TRADE
        order = Order()
        order.action = 'SELL'
        #below order quantity assumes that if there are 10 gaps (up_quantity), it would take 10 tickers / (open price of ticker if gapped 2.5% / (0.65*2)) -
        #thus, the quantity will always be less than 1x because ticker is assumed to only have gapped 2.5%, and average is always more, and even if
        #all of them were 2.5%, it still takes that and divides it by 1.3, making it smaller, AND it assumes all tickers get filled.
        #this probably takes close to half, because it accounts for splitting the account into 2 - half for gap up, half for gap down.
        #Thus, I will get rid of the 0.65 *2 aspect and replace with simply 0.65. That should more or less solve leverage problem.
        #Recall, it happens in more than one place, so both will be removed. (In initial order, stop loss, and exit on close). 
        
        order.totalQuantity = int( (up_quantity / (previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * 1.025) )/(0.65) )
        order.orderType = 'MIDPRICE'
        #order.tif = "OPG"
        #order.lmtPrice = str(round(previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * 1.025,2))
        order.eTradeOnly = False
        order.firmQuoteOnly = False
        order.orderId = app.nextorderid
        print(order.orderId)
        app.nextorderid += 1
        order.transmit = False

        app.placeOrder(order.orderId, stock_order(ticker), order)
        
        # STOP LOSS
        stop_order = Order()
        stop_order.action = 'BUY'
        stop_order.totalQuantity = int( (up_quantity / (previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * 1.025) )/(0.65) )
        stop_order.orderType = 'STP'
        stop_order.auxPrice = str(round(previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * (1.025 + STOP_PERCENT),2))
        stop_order.eTradeOnly = False
        stop_order.firmQuoteOnly = False
        stop_order.orderId = app.nextorderid
        app.nextorderid += 1
        print(order.orderId)
        stop_order.parentId = order.orderId
        stop_order.transmit = False
        app.placeOrder(stop_order.orderId, stock_order(ticker), stop_order)
        
        # EXIT ON CLOSE
        exit_order = Order()
        exit_order.action = 'BUY'
        exit_order.totalQuantity = int( (up_quantity / (previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * 1.025) )/(0.65) )
        exit_order.orderType = 'MOC'
        exit_order.eTradeOnly = False
        exit_order.firmQuoteOnly = False
        exit_order.orderId = app.nextorderid
        app.nextorderid += 1
        print(order.orderId)
        exit_order.parentId = order.orderId
        exit_order.transmit = True
        app.placeOrder(exit_order.orderId, stock_order(ticker), exit_order)
      except:
        print(ticker,'failed')


#filtered_down_list = down_list


# down_list_biggap = list(set(gap_down_df[gap_down_df['% Gap'] < -2.5].Symbol.to_list()))

# big_and_filtered_down = []
# for ticker in filtered_down_list:
#   if ticker in down_list_biggap:
#     big_and_filtered_down.append(ticker)
# total_big_filtered_down = len(down_list_biggap) #big_and_filtered_down


#Place orders
# for ticker in filtered_down_list:
#       if delay_counter == 45:
#         delay_counter = 0
#         time.sleep(1)
#       delay_counter += 3
#       try:
#         print('ticker:', ticker)
#         #print('maint margin:', margin_dict_maint[ticker], 'init margin:',margin_dict_init[ticker])
#         #print('API price, open:',open_dict[ticker], 'current:', current_dict[ticker]) #, 'previous close:', previous_day[(previous_day['Unnamed: 1'] == ticker) & (previous_day['Unnamed: 0'] == 'Close')][day_index].iloc[0])
#         print('previous close:', previous_day[previous_day['Symbol'] == ticker].close.iloc[0])
#         print('intended quantity:', int( (order_multiplier * original_balance / total_big_filtered_down) / (previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * 0.975)))
#         print('intended stop price:', str(round(previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * (0.975 + STOP_PERCENT),2)))
#         # INITIAL TRADE
#         order = Order()
#         order.action = 'BUY'
#         order.totalQuantity = int( ( down_quantity / (previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * 0.975) )/(0.65*2) )
#         order.orderType = 'MIDPRICE'
#         #order.tif = "OPG"
#         #order.lmtPrice = str(round(previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * 0.975,2))
#         order.eTradeOnly = False
#         order.firmQuoteOnly = False
#         order.orderId = app.nextorderid
#         print(order.orderId)
#         app.nextorderid += 1
#         order.transmit = False
#         app.placeOrder(order.orderId, stock_order(ticker), order)
        
#         # STOP LOSS
#         stop_order = Order()
#         stop_order.action = 'SELL'
#         stop_order.totalQuantity = int( ( down_quantity / (previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * 0.975) )/(0.65*2) )
#         stop_order.orderType = 'STP'
#         stop_order.auxPrice = str(round(previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * (0.975 - STOP_PERCENT),2))
#         stop_order.eTradeOnly = False
#         stop_order.firmQuoteOnly = False
#         stop_order.orderId = app.nextorderid
#         app.nextorderid += 1
#         print(order.orderId)
#         stop_order.parentId = order.orderId
#         stop_order.transmit = False
#         app.placeOrder(stop_order.orderId, stock_order(ticker), stop_order)
        
#         # EXIT ON CLOSE
#         exit_order = Order()
#         exit_order.action = 'SELL'
#         exit_order.totalQuantity = int( ( down_quantity / (previous_day[previous_day['Symbol'] == ticker].close.iloc[0] * 0.975) )/(0.65*2) )
#         exit_order.orderType = 'MOC'
#         exit_order.eTradeOnly = False
#         exit_order.firmQuoteOnly = False
#         exit_order.orderId = app.nextorderid
#         app.nextorderid += 1
#         print(order.orderId)
#         exit_order.parentId = order.orderId
#         exit_order.transmit = True
#         app.placeOrder(exit_order.orderId, stock_order(ticker), exit_order)
#       except:
#         print(ticker, 'failed')


#print(filtered_down_list)
#print(len(filtered_down_list))

print(filtered_up_list)
print(len(filtered_up_list))

time.sleep(30)
app._socketShutdown()
time.sleep(2)
app.disconnect()

sys.stdout.close()
sys.stderr.close()
