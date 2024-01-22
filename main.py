import pandas as pd
import json
from textblob import TextBlob
import string
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import nltk
from nltk.corpus import stopwords
stopwords.words("russian")
import ukrainian_stopwords


def preprocess(text):

    # deleted:
    # 1) special characters
    # 2) stop words
    # 3) digits

    with open('ukrainian_stopwords/stopwords_ua.txt') as f:
        stopwords_ua = f.read().splitlines()

    cached_stopwords = set(stopwords.words("english") + stopwords.words("russian") + stopwords_ua)

    for punct in string.punctuation:
        text = text.replace(punct, '')
        # Remove stopwords
    words = text.split()
    # words = [''.join(word.lower()) for word in words if word.lower() not in cached_stopwords]
    text = " ".join([i for i in words if not i.isdigit()])

    return text

# def getSubjectivity(review):
#     return TextBlob(review).sentiment.subjectivity
#     # function to calculate polarity


def getPolarity(review):
        return TextBlob(review).sentiment.polarity


# function to analyze the reviews
def analysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'


if __name__ == "__main__":

    path_to_json = 'jsons'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    output_file_path = 'sentiment_results.txt'

    df = pd.read_json('jsons/55493062-c.json', typ='series')
    print(df)

    # TEXT BLOB
    #
    for k in df:
        print(preprocess(k))
        score = TextBlob(preprocess(df)).sentiment.polarity
        print(analysis(score))
    #
    # path_to_json = 'jsons'
    # output_file_path = 'sentiment_results.txt'
    #
    # json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

    with open(output_file_path, 'w') as output_file:
        for json_file in json_files:
            with open(os.path.join(path_to_json, json_file), 'r') as file:
                data = pd.read_json(file, typ='series')

                for k in data:
                    file_name = os.path.splitext(json_file)[0]  # Extract file name without extension
                    sentiment_text = preprocess(k)
                    score = TextBlob(sentiment_text).sentiment.polarity
                    sentiment_result = analysis(score)

                    output_line = f'{file_name}.txt,{sentiment_result.lower()}\n'
                    output_file.write(output_line)
                    # print(output_line)

                    break

    # VADER

    # analyzer = SentimentIntensityAnalyzer()
    # vs = analyzer.polarity_scores('спасибо')
    # print(vs)

    # with open('sent_anal_vader', 'w') as output_file:
    #     for json_file in json_files:
    #         with open(os.path.join(path_to_json, json_file), 'r') as file:
    #             data = pd.read_json(file, typ='series')
    #
    #             for k in data:
    #                 file_name = os.path.splitext(json_file)[0]  # Extract file name without extension
    #                 sentiment_text = preprocess(k)
    #                 print(sentiment_text)
    #                 score = analyzer.polarity_scores(sentiment_text)
    #                 print(score)
    #
    #                 output_line = f'{file_name}.txt,{sentiment_result.lower()}\n'
    #                 print(output_line)
    #                 # output_file.write(output_line)
    #                 # print(output_line)
