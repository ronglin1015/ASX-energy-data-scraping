import requests
import sys
import string
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

# ASX energy credentials
username = "xxxxx"
password = "xxxxx"
URL = 'https://www.asxenergy.com.au/login'

# Start a session for persistant cookies
session = requests.session()

# This is the form data that the page sends when logging in
login_data = {'username': username,'password': password,'signin': 'Sign In'}

# Authenticate
r = session.post(URL, data=login_data)

# read url list
url_list = pd.read_excel('ASX Energy Data Scrapping.xlsx')
urls = url_list['url'].values.tolist()
code = url_list['Code'].values.tolist()

#create empty list
ls = list(range(1,len(url_list)+1))
i = 0

# get data from files
for asx_url in urls: 
    page = session.post(asx_url,login_data)
    page_content = str(page.content).replace(r"'",'')
    csv = str(page_content).split(r'\t')
    csv = str(csv).replace(r'\\n', '\n')
    csv = str(csv).replace(r"'",'')
    csv = str(csv).replace(r" ",'')
    TESTDATA=StringIO(csv)
    data = pd.read_csv(TESTDATA,index_col=False)
    data.insert(len(data.columns),column='url',value =asx_url)
    
# save dataframes to list
    ls[i] = data
    i = i +1
    
# concatenate files in list
value = pd.concat(ls,ignore_index= True)

# rename column
value = value.rename(columns={'[bdate': 'date'})

# remove rows without data
value = value[value.date != ']']

# merge two dataframes
df = pd.merge(value, url_list, how='left',on='url')

# reorder
cols = df.columns.tolist()
cols = [cols[0]] + [cols[5]] + cols[1:5] + cols[6:8]  +  cols[-10:-1] + [cols[-1]] + [cols[8]] 
df = df[cols]
df.sort_values(by=['url', 'date'])

# export result
df.to_csv('asx.csv',index=False)
