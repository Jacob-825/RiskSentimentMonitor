import numpy as np
import pandas as pd
import yfinance as yf

#Risk on currency against risk off currency, implying an increase suggests risk on market sentiment, and vice versa.
FXpairs=["NZDCHF=X","NZDJPY=X","NZDUSD=X","AUDCHF=X","AUDJPY=X","AUDUSD=X","GBPCHF=X","GBPJPY=X","GBPUSD=X","CADCHF=X","CADJPY=X","CADUSD=X","EURCHF=X","EURJPY=X","EURUSD=X"]

#Popular commodities and NASDAQ index are generally risk on. An increase suggests risk on market sentiment, and vice versa.
NYSEpairs=["COPX","^IXIC","CL=F"]

#Bond prices increasing generally follows from risk averse behaviour. Implying bond yields increasing suggests risk on market sentiment, and vice versa.
BONDpairs=["^TNX","^TYX"]

#Want to calculate SMA over 4 days of data, 192*30m = 4 days of data
def MA_FX(ticker):
    rawdata = yf.download(tickers = f"{ticker}", period = "7d", interval = "30m")
    closesum = 0
    for i in range(1,193):
        close = rawdata.iloc[-i,-3]
        closesum += close
    MA = closesum / 192
    return(MA, rawdata.iloc[-1,-3])

#for assets such as COPX, being only open in NYSE, we will need to use 52 period sma to allow exactly 4 days of data to be used
def MA_NYSE(ticker):
    rawdata = yf.download(tickers = f"{ticker}", period = "7d", interval = "30m")
    closesum = 0
    for i in range(1,53):
        close = rawdata.iloc[-i,3]
        closesum += close
    MA = closesum / 52
    return(MA, rawdata.iloc[-1,3])

#Bond data is from 8:20AM UTC-4 to 15:00 UTC-4 which would require a 320 period sma to be used on the 5m data to allow exactly 4 days of data to be used 
def MA_BOND(ticker):
    rawdata = yf.download(tickers = f"{ticker}", period = "7d", interval = "5m")
    closesum = 0
    for i in range(1,321):
        close = rawdata.iloc[-i,3]
        closesum += close
    MA = closesum / 320
    return(MA, rawdata.iloc[-1,3])

#Combine data into corresponding list
FXdata = [MA_FX(i) for i in FXpairs]
NYSEdata = [MA_NYSE(i) for i in NYSEpairs]
BONDdata = [MA_BOND(i) for i in BONDpairs]

directions=[]

#Combine the above lists into dataframe structure for a neater and more managable output
dataframe = pd.concat([pd.DataFrame(FXdata, index = [i.removesuffix('=X') for i in FXpairs]), pd.DataFrame(NYSEdata, index = NYSEpairs), pd.DataFrame(BONDdata, index = BONDpairs)])
dataframe.columns = ['MA', 'Price']

#Work out relative directions for each security
for i in dataframe.index.values:
    if dataframe.loc[i, 'Price'] > dataframe.loc[i, 'MA']:
        directions.append(1)
    else:
        directions.append(-1)
       
dataframe['Relative Direction'] = directions    

#Append mean to identify overall market risk sentiment
pd.concat([dataframe, pd.DataFrame([dataframe['Relative Direction'].mean()], columns=['Relative Direction'], index=["Overall risk sentiment"])])