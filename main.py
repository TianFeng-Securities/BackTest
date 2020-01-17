#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[13]:


from tqdm import tqdm


# In[16]:


import numpy as np


# In[56]:


pe_data = pd.read_excel("投资收益压力测试.xlsx",sheet_name='投资收益压力测试',usecols=['pe','分位','price'])


# In[10]:


pe_data.head()


# In[ ]:


####首先，以2007-2011为模拟回测市场前期，从2012到2019年开始回测，index从1212开始


# In[59]:


def back_test(df:pd.DataFrame,low,high,time=1):##low，high为分位区间端点,time为投资时间,以月为单位
    gains = []
    for index,row in tqdm(df.iterrows()):
        if row['分位']>low and row['分位']<=high:
            next_index = index+time*20
            if index+time*20>df.index[-1]:
                next_index = df.index[-1]
            gains.append(df['price'][next_index]/df['price'][index]-1)###将每一次收益添加至gains
    ###返回值为gains的平均值，还有胜率
    temp_array = np.array(gains)
    temp_array[temp_array>0] = 1
    temp_array[temp_array<0] = 0
    return np.mean(gains),np.mean(temp_array)


# In[73]:


resul_pe = pd.DataFrame(index=[0.25,0.5,0.75,1],columns=[1,3,6,12,18,24,32,36])


# In[74]:


for i in [1,3,6,12,18,24,32,36]:
    for low,high in [(0,0.25),(0.25,0.5),(0.5,0.75),(0.75,1)]:
        gain,acc = back_test(pe_data.loc[1212:,:],low,high,i)
        resul_pe[i][high] = gain


# In[75]:


resul_pe.to_excel("pe收益.xlsx")


# In[72]:


resul_pe


# In[ ]:




