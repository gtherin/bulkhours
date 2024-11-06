import pandas as pd
import numpy as np
import re

from .data_parser import DataParser


def _clean_tweet(text):
    import emoji
    import html.parser
    
    output = re.sub('http[\w\d\D./]+', '', text).strip() #remove url
    output = output.encode('ascii', 'ignore').decode('ascii') # remove emoji
    output = re.sub('\s\s+', ' ', output).strip() # remove white spaces
    output = html.unescape(output) # escape html
    output = output.lower() # lower case

    return output

def clean_tweet(df):
    df['clean_text'] = df['text'].apply(lambda x: _clean_tweet(x))
    
    return df


def _get_mention_handle(text):
    output = list(set(re.findall('@\w+', text)))
    
    return output

def get_mention_handle(df):
    df['handles_mentioned'] = df['text'].apply(lambda x: _get_mention_handle(x))
    
    return df

def _get_hashtag(text):    
    output = list(set(re.findall('#\w+', text)))
    return output

def get_hashtag(df):
    
    df['hashtags'] = df['text'].apply(lambda x: _get_hashtag(x))
    
    return df


def clean_column_names(df):
    df.columns = [i.lower() for i in df.columns]
    
    return df



def get_date_attr(df):
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    
    return df


def format_flags(df):
    df['isflagged'] = df['isflagged'].apply(lambda x: True if x == 't' else False)
    df['isdeleted'] = df['isdeleted'].apply(lambda x: True if x == 't' else False)
    df['isretweet'] = df['isretweet'].apply(lambda x: True if x == 't' else False)
    
    return df


def drop_tweets(df):
    df = (df
          .loc[(df['clean_text'] != '') 
               & (df['year'].between(2012,2021))
               & (df['isretweet'] == False)
               & ~(df['handles_mentioned'].apply(lambda x: '@realDonaldTrump' in x))
              ]
          .reset_index(drop = True))
    
    return df


def get_retweets(df):
    df.loc[(df['text'].str.contains('^RT @|^\"RT @')), 'isretweet'] = True
    
    return df


@DataParser.register_dataset(
    label="donald.trump.tweets",
    summary="Donald Trup tweets",
    category="text",
    ref_source="https://www.kaggle.com/code/edwintyh/donald-trump-s-tweets-sentiment-analysis-model",
    enrich_data="https://github.com/gtherin/bulkhours/blob/main/bulkhours/data/text.py",
)
def get_poverty(self, timeopt=None):

    import kagglehub
    from transformers import pipeline
    import pandas as pd
    import html.parser
    pd.set_option('display.max_colwidth', None)

    # Get the Donald_Trump's_Tweets data
    df = pd.read_csv(kagglehub.dataset_download('codebreaker619/donald-trump-tweets-dataset') + "/tweets.csv")
    df = (df
      .pipe(clean_column_names)
      .pipe(clean_tweet)
      .pipe(get_date_attr)
      .pipe(get_hashtag)
      .pipe(get_mention_handle)
      .pipe(format_flags)
      .pipe(get_retweets)
      .pipe(drop_tweets))
    return df

