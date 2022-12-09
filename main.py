import requests
import smtplib
import os

my_email = os.environ.get("MY_EMAIL")
my_password = os.environ.get("MY_PASSWORD")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
NEWS_END_POINT = 'https://newsapi.org/v2/everything'
COMPANY_NAME = 'Tesla'

STOCK_END_POINT = 'https://www.alphavantage.co/query'
STOCK_API_KEY = os.environ.get("STOCK_APY_KEY")
STOCK = 'TSLA'
stock_parameters = {
    'function': 'GLOBAL_QUOTE',
    'symbol': STOCK,
    'apikey': STOCK_API_KEY
}

# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response = requests.get(url=STOCK_END_POINT, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()['Global Quote']
# print(stock_data)
change_percent = stock_data['10. change percent']

formatted_change_percent = float(change_percent.replace("%", ""))
print(formatted_change_percent)
if formatted_change_percent > 0:
    icon = '🔺'
else:
    icon = '🔻'

if abs(formatted_change_percent) >= 2:
    news_parameters = {
        'apiKey': NEWS_API_KEY,
        'language': 'en',
        'sortBy': 'relevancy',
        'q': COMPANY_NAME
    }

    # print("Get News")  # check
    response = requests.get(url=NEWS_END_POINT, params=news_parameters)
    response.raise_for_status()
    top_three_articles = response.json()['articles'][:3]  # slices the top three articles
    # print(top_three_articles)

    articles_list = [f"Headline: {article['title']}.\nBrief: {article['description']}\nURL: {article['url']}"
                     for article in top_three_articles]  # !!!! review this
    # print(articles_list)


    for article in articles_list:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
            connection.ehlo()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject: {STOCK}:{icon}{abs(formatted_change_percent)}%\n\n"
                    f"Read Why:\n{article}".encode()   # fixed
            )
            print('Email sent!')


