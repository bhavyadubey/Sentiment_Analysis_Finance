import re
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import Constants as con

read_csv_path = './streamed_tweets/new_tweets.csv'
write_csv_path = './streamed_tweets/new_clean_tweets.csv'


df=pd.read_csv(read_csv_path,encoding='utf-8',header=0)
print(df.head(10))
print(df.shape,df.columns)

# nltk.download('stopwords')
# nltk.download('wordnet')
wordnet_lemmatizer = WordNetLemmatizer()


def cleanText(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r'https?:\/\/\S+', '', text)
    return text


def splitTweet(text):
    return text.split()

STOPWORDS = set(stopwords.words('english'))
def remove_stopwords(l):
    return [word for word in l if len(word) > 2 and word not in STOPWORDS]


def lemmatization(l):
    temp = []
    for i in l:
        temp.append((wordnet_lemmatizer.lemmatize(i)).lower())
    return " ".join(temp)


def getCompanyName(tweet):
    for k,v in hash_tag_list.items():
        for i in v:
            if(i.lower() in tweet.lower()):
                return k

# add company column
hash_tag_list = con.hash_tag_list
for i in hash_tag_list.keys():
    for j in range(len(hash_tag_list[i])):
        hash_tag_list[i][j] = hash_tag_list[i][j].lower()

def removeNullCompany(row):
     if(row.split(",")[1] != None):
        return row

df['Company'] = df['Tweet'].apply(getCompanyName)

print('after\n',df.head(10))
# clean the tweet
df['Tweet'] = df['Tweet'].apply(cleanText)

# split each tweet by space and make list
df['Split_tweet'] = df['Tweet'].apply(splitTweet)

# remove stopwords
df['Clean_tweet'] = df['Split_tweet'].apply(remove_stopwords)

# lemmatize tweet
df['Lemmatized_tweet'] = df['Clean_tweet'].apply(lemmatization)

# remove empty tweets row
df = df[df['Lemmatized_tweet'] != '']

# remove empty company tweets
df = df.dropna()

# write clean text into another csv
df_new = pd.DataFrame({'TimeStamp': df['TimeStamp'], 'Company': df['Company'], 'Clean_text': df['Lemmatized_tweet']})
df_new.to_csv(write_csv_path, index=False)

print(df_new['Company'].head())
