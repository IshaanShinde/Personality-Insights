from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url_finviz = "https://finviz.com/quote.ashx?t="

companies = {'Amazon': 'AMZN',
             'Nvidia': 'NVDA',
             'META'  : 'META',
             'AMD'   : 'AMD',
             'GitLab': 'GTLB'}

# Fetching the table of articles for all the companies

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

# Parsing the tables fetched into a dataframe
data = []
for ticker, news_articles in table_news_articles.items():
    for row in news_articles.findAll('tr'):
        
        title = row.a.text
        
        timestamp = row.td.text.split(' ')
        if len(timestamp) == 1:
            time = timestamp[0]
        else:
            date = timestamp[0]
            time = timestamp[1]

        data.append([ticker, date, time, title])

print(data)