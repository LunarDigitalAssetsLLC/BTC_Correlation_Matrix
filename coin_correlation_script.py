
# coding: utf-8

# In[1]:


'''
This script is for generating a 90-Day correlation coefficient chart of Top 100 coins.

Dependencies for data prep: Numpy, Pandas
Dependencies for data retrieval and processing: requests, json, time
Dependencies for data viz: plotly, cufflinks

File dependencies: top100cointlist.csv (keep in same directory as script, otherwise edit script to correct path)
'''


# In[2]:


# import libraries

import numpy as np
import pandas as pd

import requests
import json
import time

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='chu.garrick', api_key='B0TUQry7k4MGzjeu7zxS')
import cufflinks as cf


# In[3]:


# load in file with coin tickers, converts into iterable list
#coin_list = pd.read_csv('top100coinlist.csv')
#coin_tickers = list(coin_list['short'])


# In[9]:


# retrieve live list of top 100 coins

try: 
    print('Getting Top 100 Coin Data...')
    list = requests.get('https://min-api.cryptocompare.com/data/top/totalvol?limit=100&tsym=USD')
    json = list.json()
    print('Success!')
except:    
    import sys
    sys.exit('Could not obtain Top 100 Coin Data. Please wait a few moments and retry. Aborting script...')


# In[14]:


# process response data

coin_tickers = []

for coin in range(len(json['Data'])):
    coin_tickers.append(json['Data'][coin]['CoinInfo']['Internal'])


# In[15]:


# creates empty Pandas DataFrame, iterates over list of coins and inputs into DF
# limit currently set to 60, indicates 60 day history in this API call
print('Fetching Coin Data... This may take a minute or two.')
daily_change = pd.DataFrame([])

for coin in coin_tickers:
    try: 
        url = 'https://min-api.cryptocompare.com/data/histoday?fsym='+coin+'&tsym=USD&limit=60'
        response = requests.get(url)
        json = response.json()
        temp_df = pd.DataFrame(json['Data'])
        
        col_header = coin
        compute = (temp_df['close'] - temp_df['open'])/temp_df['open']
        daily_change[col_header] = compute
        time.sleep(.001)   
       
    
    except:
        print('The ticker '+str(coin)+' was not found. Skipping...')


# In[16]:


# convert DataFrame into correlation matrix
corrmat = daily_change.corr(method='pearson')


# In[22]:


# plot the corr matrix in plotly

corrmat.iplot(kind='heatmap', colorscale='spectral', title='Daily % Change Correlations of Top 100 Coins (60 Days)', 
             size=16, theme='pearl', dimensions=(1000,1000), showticklabels=True, autorange='reversed')

print('See URL for heatmap: https://plot.ly/~chu.garrick/7.embed')

