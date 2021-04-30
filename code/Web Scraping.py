#!/usr/bin/env python
# coding: utf-8

# ## Dhruv Patel
# ## dhruv692000@gmail.com

# In[2]:


import requests
import urllib.request 
from urllib.request import urlopen
import time
import datetime as dt
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import math as m


# In[3]:


url = "https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=325&Tx_State=0&Tx_District=0&Tx_Market=0&DateFrom=01-Mar-2015&DateTo=01-Apr-2015&Fr_Date=01-Mar-2015&To_Date=01-Apr-2015&Tx_Trend=0&Tx_CommodityHead=Almond(Badam)&Tx_StateHead=--Select--&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--"


# In[4]:


response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


# In[5]:


soup


# In[6]:


type(soup)


# In[5]:


day_diff_15 = dt.timedelta(days = 15)
day_diff_1 = dt.timedelta(days = 1)
#start_date = '01-jan-18'
#end_date = '28-feb-21'
start_date = datetime.strptime('01-jan-18', '%d-%b-%y')
end_date = datetime.strptime('28-feb-21', '%d-%b-%y')
a = start_date
dat_lst=[]
while True:
    str_d = a 
    end_d = a + day_diff_15
    if end_d > end_date:
        dat_lst.append([str_d.strftime('%d-%b-%y'), end_date.strftime('%d-%b-%y')])
        break
    dat_lst.append([str_d.strftime('%d-%b-%y'),end_d.strftime('%d-%b-%y')])
    a = end_d + day_diff_1
    
dat_lst


# In[9]:


lsdiv = soup.findAll("div", {"class": "commodity"})
commo_value_text_dict = {}
print(lsdiv)


# In[10]:


opt_tags = lsdiv[1].findAll('option')
for i in opt_tags:
    commo_value_text_dict[i['value']] = i.text
    
del commo_value_text_dict['0']
commo_value_text_dict


# In[6]:


def getdf(comm, ds, de):
    column = []
    url = "https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity={0}&Tx_State=0&Tx_District=0&Tx_Market=0&DateFrom={1}&DateTo={2}&Fr_Date=01-Mar-2015&To_Date=01-Apr-2015&Tx_Trend=0&Tx_CommodityHead=Almond(Badam)&Tx_StateHead=--Select--&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--".format(comm, ds, de)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tbl = soup.findAll("table",{"id" : "cphBody_GridPriceData"})
    cols = tbl[0].findAll("tr")
    for ir in cols:
        ii = ir.findAll("th")
        for j in ii:
            if j.text !="":
                column.append(j.text)
    dtfrm = pd.DataFrame(columns=column)
    return dtfrm, column


# In[13]:


comm_number_list = sorted(list(commo_value_text_dict.keys()))
for i in comm_number_list:
    if i in already_done:
        continue
    time.sleep(15)
    print('item ', i,': ',commo_value_text_dict[str(i)], '\n')
    main_dfrm, colu = getdf(i, dat_lst[0][0], dat_lst[0][1])
    rowcount = 0
    inner_dfrm = main_dfrm.copy()
    for sd, ed in dat_lst:
        url = "https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity={0}&Tx_State=0&Tx_District=0&Tx_Market=0&DateFrom={1}&DateTo={2}&Fr_Date=01-Mar-2015&To_Date=01-Apr-2015&Tx_Trend=0&Tx_CommodityHead=Almond(Badam)&Tx_StateHead=--Select--&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--".format(i, sd, ed)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        tbl = soup.findAll("table",{"id" : "cphBody_GridPriceData"})
        
        rows = tbl[0].findAll("tr")
        data = []
        for ir in rows:
            ii = ir.findAll("td")
            for j in ii:
                if j.text != "":
                    data.append(j.text)
        data2 =[]
        for ida in data:
            ida = ida.strip()
            ida = ida.strip('\r')
            ida = ida.strip('\n')
            ida = ida.strip('\t')
            if ida != '':
                data2.append(ida)
    
        ind=1
        strd = ''
        
        for iet in range(len(data2)):
            inner_dfrm.loc[m.floor(iet/10), colu[m.floor(iet%10)]] = data2[iet]
        main_dfrm = main_dfrm.append(inner_dfrm, ignore_index = True).copy()
        #print(main_dfrm)
    com_nam = str(commo_value_text_dict[str(i)])
    com_nam = com_nam.replace('/', ' ')    
    main_dfrm.to_csv('D:/Folder/main/!!Nirma/Side_Projects/Data analysis/Auto generated csv/'+com_nam+'.csv')    
    already_done.append(i)
    

