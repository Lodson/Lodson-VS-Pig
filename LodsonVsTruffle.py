# %%
import bt
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta
matplotlib.use('TkAgg') #Use 'MacOSX' if not on Windows 
#%matplotlib inline

# @Lodson "LeChaffeur" Portfolio:'

pos = {} #Set Up Core Positions for Each Rebalance Date
pos[pd.to_datetime('2021-11-09')] = dict.fromkeys(['SPY','XLF','BITO','EEM','EFA','VNQ','TLT','QQQ','LQD','TSM','SMH','EMB','HEFA','AAPL','MSFT','AMZN','GOOGL','META','NVDA', 'VGK'], -0.75) | dict.fromkeys(['U-UN.TO','URNM','GLD','SLV','SHV','BIL','SHY','STIP','FENY','UUP'], 0.9)
for k in pos: pos[k].update((x, y*1/len(pos[k])) for x, y in pos[k].items()) # Weight of Positions

# Portfolio distribution: 20% CASH - 30% LONG - 50% SHORT
 
# Explaining the 0,75 and 0,9 to short and long positions above:
# For len(pos[k]= 30 (total tickers) gives short position of 20 tickers should result in 50% of total portfolio gives us:
# 0,75 = 0,5 (50%) * 30 (total tickers) / 20 (total tickers being short)

# Same goes for the long position being 30% of total portfolio:
# 0,9 = 0,3 (30%) * 30 (total tickers) / 10 (total tickers being long)

lodson = pd.DataFrame.from_dict(pos,orient='index').fillna(0.0) 
lodson.index.name = 'Date'
lodsonprices = bt.get(list(lodson), clean_tickers=False, start=lodson.first_valid_index(), end=date.today())

# @AlphaTruffle Pig Portfolio:

parpos = {} #Set Up Core Positions for Each Rebalance Date for @AlphaTruffle
parpos[pd.to_datetime('2021-11-09')] = dict.fromkeys(['TLT','EMB','IWM','DIA','SPY','QQQ','EEM','VGK','REM','VNQ','BITO','LQD','HYG','IGSB','AAPL','AMZN','FB','GOOGL','MSFT','NVDA','GDX','CPER','GSG'], -1.0) | dict.fromkeys(['IEI','SHY','SHV','BIL','GLD','UUP','FXF','FXY','VXX'], 1.0)
parpos[pd.to_datetime('2022-02-24')] = dict.fromkeys(['TLT','EMB','IWM','DIA','SPY','QQQ','EEM','VGK','REM','VNQ','BITO','LQD','HYG','IGSB','AAPL','AMZN','FB','GOOGL','MSFT','NVDA'], -1.0) | dict.fromkeys(['IEI','SHY','SHV','BIL','UUP','FXF','FXY','VXX','GLD'], 1.0)
parpos[pd.to_datetime('2022-03-31')] = dict.fromkeys(['TLT','EMB','IWM','DIA','SPY','QQQ','EFA','EEM','VGK','REM','VNQ','SMH','JNK','IJH','BITO','LQD','HYG','IGSB','XLF','EUFN','AAPL','AMZN','FB','GOOGL','MSFT','NVDA'], -0.75) | dict.fromkeys(['BIL','SHV','SHY','IEI','STIP','UUP','FXF','FXY','GLD','SLV'], 0.75)
parpos[pd.to_datetime('2022-05-20')] = dict.fromkeys(['TLT','EMB','IWM','DIA','SPY','QQQ','EFA','EEM','VGK','REM','VNQ','SMH','JNK','IJH','BITO','LQD','HYG','IGSB','XLF','EUFN','AAPL','AMZN','FB','GOOGL','MSFT','NVDA'], -0.50) | dict.fromkeys(['BIL','SHV','SHY','IEI','STIP','UUP','FXF','FXY','GLD','SLV'], 0.50)
for k in parpos: parpos[k].update((x, y*1/len(parpos[k])) for x, y in parpos[k].items()) #Equal Weight Core Positions                                   
parpos[pd.to_datetime('2022-05-20')] = parpos[pd.to_datetime('2022-05-20')] | dict.fromkeys(['ES=F','NQ=F','RTY=F'], 0.05) #Add Hedges Where Applicable
pig = pd.DataFrame.from_dict(parpos,orient='index').fillna(0.0) 
pig.index.name = 'Date'
pigprices = bt.get(list(pig), clean_tickers=False, start=pig.first_valid_index(), end=date.today())

# Backtesting setup
report = bt.run(bt.Backtest(data=lodsonprices, strategy=bt.Strategy('@Lodson Theoretic LeCaffeur Portfolio', algos=[bt.algos.SelectAll(), bt.algos.WeighTarget(lodson), bt.algos.Rebalance()])),
                bt.Backtest(data=pigprices, strategy=bt.Strategy('@AlphaTruffle Pig Portfolio', algos=[bt.algos.SelectAll(), bt.algos.WeighTarget(pig), bt.algos.Rebalance()])))

#print(pos)
#print(parpos)
report.display()
report.plot()
plt.title('Lodson Theoretic "LeChaffeur" Portfolio ETF --VS-- @AlphaTruffle Pig  Since Inception (9 Nov 2021)')
plt.show()
# %%
