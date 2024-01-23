from django.http import JsonResponse
import requests
import urllib
from urllib.parse import quote_plus
import mysql.connector
from my_settings import NEWS_API_KEY, DATABASES
import sys
sys.path.append(r"C:/Users/김유진/OneDrive/문서/GitHub/SOLUX_Paperie/Backend/paperie/paperie")
import my_settings

def search_news(request):

    query = request.GET.get('q')

    url = ('https://newsapi.org/v2/everything?'
           f'q={quote_plus(query)}&'
           'sortBy=popularity&'
           f'apiKey={NEWS_API_KEY}&'
           'pageSize=20')

    response = requests.get(url)

    # MySQL 연결
    connection = mysql.connector.connect(
        host=DATABASES['default']['HOST'],
        user=DATABASES['default']['USER'],
        password=DATABASES['default']['PASSWORD'],
        database=DATABASES['default']['NAME']
    )

    # 커서 생성
    cursor = connection.cursor()

    try:
        # 데이터 삽입
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
        
        response_data = {
            'message': 'Data saved to MySQL successfully.'
        }

    except Exception as e:
        response_data = {
            'error': str(e)
        }

    finally:
        # 연결 및 커서 닫기
        connection.close()
        cursor.close()

    return JsonResponse(response_data)