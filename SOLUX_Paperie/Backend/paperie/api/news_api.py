import requests
import mysql.connector
import my_settings

url = ('https://newsapi.org/v2/everything?'
       'q=keyword&'
       'sortBy=popularity&'
       'apiKey={my_settings.NEWS_API_KEY}')

#DATABASES = my_settings.DATABASES

response = requests.get(url)

# Check the response status
if response.status_code == 200:
    news_data = response.json()
    print(news_data)
else:
    print(f"Error: {response.status_code}")
    print(response.text)