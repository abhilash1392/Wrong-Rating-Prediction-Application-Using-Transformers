# Importing the libraries
import pandas as pd 
import numpy as np
from transformers import pipeline 
from autocorrect import Speller


# For checking the spellings 
spell = Speller()
def spelling_checker(x):
    return spell(x)
# Sentiment analyzer from huggingface transformer library
sentiment_analyzer = pipeline('sentiment-analysis')
def check_sentiment(x):
    return sentiment_analyzer(x)[0]['label']

def check_rating(x):
    if x <=3:
        return 'NEGATIVE'
    else:
        return 'POSITIVE'

def check_csv_file(file_path):
    df = pd.read_csv(file_path)
    df = df[df['Text'].isna()==False]
    df.reset_index(drop=True,inplace=True)
    df['cleaned_text'] = -1
    for i in range(len(df.index)):
        df.loc[i,'cleaned_text'] = spelling_checker(df.loc[i,'Text'])

    df['sentiment_detected_on_review'] = -1
    for i in range(len(df.index)):
        df.loc[i,'sentiment_detected_on_review'] = check_sentiment(df.loc[i,'cleaned_text'])

    df['sentiment_detected_on_stars'] = -1
    for i in range(len(df.index)):
        df.loc[i,'sentiment_detected_on_stars'] = check_rating(df.loc[i,'Star'])

    df['wrong_rating']=(df.sentiment_detected_on_review!=df.sentiment_detected_on_stars)
    new_df = df[df['wrong_rating']==True]
    new_df.reset_index(inplace=True,drop=True)
    new_df.to_csv('output.csv',index=False)


def check_user_input(text,star):
    cleaned_text = spelling_checker(text)
    sentiment_detected = check_sentiment(cleaned_text) 
    sentiment_rating = check_rating(star)
    if sentiment_detected==sentiment_rating:
        return text,star,False
    else:
        return text,star,True



