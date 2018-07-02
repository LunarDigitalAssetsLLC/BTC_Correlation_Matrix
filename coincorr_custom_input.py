
# coding: utf-8

# In[9]:


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


# In[10]:


#takes in user input for coin, will need to build this out further to do input validation

num_coins = int(input('How many coins to find a correlation for? (Minumum of 2) '))

coin_tickers = []

for i in range(0, num_coins):
    print('For symbol/ticker look up, visit Cryptocompare.com')
    coin_tickers.append(input('Provide  symbol/ticker for coin #{}: '.format(i+1)))
    

period = input('Enter time period in Days (max is 2000)' )


# In[11]:


daily_change = pd.DataFrame([])


for coin in coin_tickers:
    try: 
        url = 'https://min-api.cryptocompare.com/data/histoday?fsym='+coin+'&tsym=USD&limit='+period
        response = requests.get(url)
        json = response.json()
        temp_df = pd.DataFrame(json['Data'])
        
        col_header = coin
        compute = (temp_df['close'] - temp_df['open'])/temp_df['open']
        daily_change[col_header] = compute
        time.sleep(.001)   
       
    
    except:
        print('The ticker '+str(coin)+' was not found. Skipping...')


# In[12]:


# convert DataFrame into correlation matrix
corrmat = daily_change.corr(method='pearson')


# In[14]:


# plot the corr matrix in plotly

corrmat.iplot(kind='heatmap', colorscale='spectral', title='Daily % Change Correlations of {} Coins ({} Days)'.format(num_coins, period), 
             size=16, theme='pearl', dimensions=(1000,1000), showticklabels=True, autorange='reversed')

print('See URL for heatmap: https://plot.ly/~chu.garrick/')

