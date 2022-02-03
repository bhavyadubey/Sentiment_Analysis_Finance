import re
import pandas as pd
import numpy as np
import nltk

import Constants as con

df=pd.read_csv('new_tweets.csv',encoding='utf-8',header=None)
print(df.head(10))

df.columns=cols
hash_tag_list = con.hash_tag_list
tweet=[]
time_of=[]
company=[]

for k in df.values:
    for i in hash_tag_list:
        if i.lower() in str(k[1].lower()):
            company.append(str(i))
            tweet.append(k[1])
            time_of.append(pd.to_datetime(k[0]))

new_df=pd.DataFrame()
new_df['company']=pd.Series(company).values
new_df['Tweet_text']=pd.Series(tweet).values
new_df['TimeStamp']=pd.Series(time_of).values

print(new_df.head(),new_df.shape)
new_df.to_csv('Company_tweets.csv',mode = 'a',index=False)
