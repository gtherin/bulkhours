import pandas as pd
import numpy as np
import re

from .data_parser import DataParser


def _clean_tweet(text):
    #import emoji
    import html.parser
    
    output = re.sub(r'http[\w\d\D./]+', r'', text).strip() #remove url
    output = output.encode('ascii', 'ignore').decode('ascii') # remove emoji
    output = re.sub(r'\s\s+', r' ', output).strip() # remove white spaces
    output = html.unescape(output) # escape html
    output = output.lower() # lower case

    return output

def clean_tweet(df):
    df['clean_text'] = df['text'].apply(lambda x: _clean_tweet(x))
    
    return df


def _get_mention_handle(text):
    output = list(set(re.findall(r'@\w+', text)))
    
    return output

def get_mention_handle(df):
    df['handles_mentioned'] = df['text'].apply(lambda x: _get_mention_handle(x))
    
    return df

def _get_hashtag(text):    
    output = list(set(re.findall(r'#\w+', text)))
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
def get_tweets(self, timeopt=None):

    import kagglehub
    #from transformers import pipeline
    #import pandas as pd
    #import html.parser
    #pd.set_option('display.max_colwidth', None)

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


def get_sentiments(hf_pipeline, text_lists):
    emotions_data = []
    for t in text_lists:
        emotions_data.append(pd.DataFrame(hf_pipeline(t)[0]).set_index("label").T)
    data = pd.concat(emotions_data, axis=0).reset_index(drop=True)
    return data


def en2fr(emotions):
    en2fr = {'anger': 'colère', 'disgust': 'dégout', 'fear': 'peur', 'joy': 'joie', 'neutral': 'neutre', 'sadness': 'tristesse', 'surprise': 'surprise', 
            'anticipation':'anticipation', 'trust':'confiance'}
    if type(emotions) == str:
        return en2fr[emotions]
    return [en2fr[e] for e in emotions]

def en2icons(emotions):
    # 🤢 is replaced by 😡 ERROR: {NAUSEATED FACE}
    en2icons = {'anger': '😠', 'disgust': '😡', 'fear': '😨', 'joy': '😄', 'neutral': '😐', 'sadness': '😢', 'surprise': '😲', 'anticipation': '👍', 'trust': '🤝'}
    if type(emotions) == str:
        return en2icons[emotions]
    return [en2icons[e] for e in emotions]



