import os
import sys
import urllib.request
import json
import mysql.connector
import datetime
import requests

from django.http import JsonResponse

sys.path.append(r"C:/Users/김유진/OneDrive/문서/GitHub/SOLUX_Paperie/Backend/paperie/paperie")
import my_settings

def search_books(request):
    client_id = my_settings.NAVER_CLIENT_ID
    client_secret = my_settings.NAVER_CLIENT_SECRET

    query = request.GET.get('query')  # 검색어 가져오기

    url = "https://openapi.naver.com/v1/search/book?query=" + urllib.parse.quote(query)  # JSON 결과

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    request = urllib.request.Request(url, headers=headers)

    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        data = json.loads(response_body.decode('utf-8'))

        # MySQL 연결
        connection = mysql.connector.connect(
            host=my_settings.DATABASES['default']['HOST'],
            user=my_settings.DATABASES['default']['USER'],
            password=my_settings.DATABASES['default']['PASSWORD'],
            database=my_settings.DATABASES['default']['NAME']
        )
        cursor = connection.cursor()

        # lastBuildDate 가져오기
        last_build_date = data.get('lastBuildDate')

        # MySQL에 저장할 날짜 형식으로 변환
        last_build_date = datetime.datetime.strptime(last_build_date, "%a, %d %b %Y %H:%M:%S +0900")
        last_build_date = last_build_date.strftime("%Y-%m-%d")

        # 도서 정보를 MySQL에 삽입
        for book in data['items']:
            title = book['title']
            author = book['author']
            publisher = book['publisher']
            pubdate = book['pubdate']
            discount = book['discount']
            isbn = book['isbn']
            image = book['image']

            if 'url' in book:
                url = book['url']
            else:
                url = None

            # MySQL에 데이터 삽입하는 쿼리
            insert_query = "INSERT INTO book (title, author, publisher, pubdate, discount, isbn, image, url, searchdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            insert_data = (title, author, publisher, pubdate, discount, isbn, image, url, last_build_date)

            # 쿼리 실행
            cursor.execute(insert_query, insert_data)

        # 변경 사항 커밋
        connection.commit()

        # MySQL 연결 종료
        cursor.close()
        connection.close()

        return JsonResponse({'message': '데이터를 MySQL에 성공적으로 저장했습니다.'})
    else:
        return JsonResponse({'error': 'API 요청에 실패했습니다.'})