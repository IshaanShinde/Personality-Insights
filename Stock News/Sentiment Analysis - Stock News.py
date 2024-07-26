import pandas as pd
import matplotlib.pyplot as plt

# import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url_finviz = "https://finviz.com/quote.ashx?t="

companies = {'Amazon': 'AMZN',
             'Nvidia': 'NVDA',
             'META'  : 'META',
             'AMD'   : 'AMD',
             'GitLab': 'GTLB'}

# Parsing the page to fetch table of articles for all the companies
table_news_articles = {}

for company, ticker in companies.items():
    url = url_finviz + ticker

    req = Request(url = url, headers = {'user-agent': 'personal_news_analysis'})
    response = urlopen(req)

    html = BeautifulSoup(response, features = "html.parser")

    news_table = html.find(id = 'news-table')
    table_news_articles[ticker] = news_table
    
    # break the loop after the first iteration while testing to avoid spamming the website
    break

# extracting the required elements from the table of articles
data = []

for ticker, news_articles in table_news_articles.items():
    for row in news_articles.findAll('tr'):
        
        title = row.a.text.strip()
        
        timestamp = row.td.text.strip().split(' ')

        if len(timestamp) == 1:
            time = timestamp[0]
        else:
            date = timestamp[0]
            time = timestamp[1]

        data.append([ticker, date, time, title])

# converting the extracted information into a pandas dataframe
dataframe = pd.DataFrame(data, columns = ['ticker', 'date', 'time', 'title'])

# adding the compund score by title to the dataframe
vader = SentimentIntensityAnalyzer()

vader_func = lambda title: vader.polarity_scores(title)['compound']
dataframe['compound'] = dataframe['title'].apply(vader_func)

# converting the date into the correct dtype
# dataframe['date'] = pd.to_datetime(dataframe.date).dt.date


def test():
    print(dataframe.head())
    print(f'\ndatetime\n')
    print(dataframe[['date', 'time']].head(50))
    print(f'\ntitles\n')
    print(dataframe['title'].head())
    return None

test()