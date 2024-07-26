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
    # break

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

# adding the scores by title to the dataframe
vader = SentimentIntensityAnalyzer()

vader_pos = lambda title: vader.polarity_scores(title)['pos']
dataframe['pos'] = dataframe['title'].apply(vader_pos)

vader_neu = lambda title: vader.polarity_scores(title)['neu']
dataframe['neu'] = dataframe['title'].apply(vader_neu)

vader_neg = lambda title: vader.polarity_scores(title)['neg']
dataframe['neg'] = dataframe['title'].apply(vader_neg)

vader_compound = lambda title: vader.polarity_scores(title)['compound']
dataframe['compound'] = dataframe['title'].apply(vader_compound)

# converting the date into the correct dtype
def parse_date(date_string):
    if date_string == 'Today':
        return pd.Timestamp.today().date()
    else:
        try:
            return pd.to_datetime(date_string, format = '%b-%d-%y', errors = 'coerce').date()
        except Exception as e:
            print(f"Error Parsing Date: '{date_string}': {e}")
            return pd.NaT
        
dataframe['date'] = dataframe['date'].apply(parse_date)

# saving the dataframe
dataframe.to_csv(f'Finviz Stock News {pd.Timestamp.today().date()}.csv')