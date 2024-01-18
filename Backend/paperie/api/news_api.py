import requests
import mysql.connector
import sys
sys.path.append("#")
import my_settings

url = ('https://newsapi.org/v2/everything?'
       'q="turtle"&'
       'sortBy=popularity&'
       f'apiKey={my_settings.NEWS_API_KEY}')

response = requests.get(url)

connection = mysql.connector.connect(
    host = my_settings.MYSQL_HOST,
    user = my_settings.MYSQL_USER,
    password = my_settings.MYSQL_PASSWORD,
    database = my_settings.MYSQL_DATABASE
    )

#커서 생성
cursor = connection.cursor()


try:
    #데이터 삽입
    news_data = response.json()
    articles = news_data.get('articles', [])

    for article in articles:
        title = article.get('title', '')
        author = article.get('author', '')
        url = article.get('url', '')
        publish = article.get('publishedAt', '')
        name = article.get('source', {}).get('name', '')

        # MySQL에 데이터 삽입하는 쿼리
        insert_query = "INSERT INTO news (title, author, url, publish, name) VALUES (%s, %s, %s, %s, %s)"
        data = (title, author, url, publish, name)

        # 쿼리 실행
        cursor.execute(insert_query, data)

        # 변경 사항을 커밋
        connection.commit()
        print("Data saved to MySQL successfully.")

except Exception as e:
        print(f"Error: {e}")

finally:
    # 연결 및 커서 닫기
    connection.close()
    cursor.close()


# Check the response status
if response.status_code == 200:
    news_data = response.json()
    print(news_data)
else:
    print("Error:{response.status_code}")
    print(response.text)