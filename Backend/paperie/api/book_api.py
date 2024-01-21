import os
import sys
import urllib.request
import json
import mysql.connector
sys.path.append(r"C:\Users\한지수\Documents\GitHub\한지수\SOLUX_Paperie(4)\Backend\paperie")
import my_settings
import requests

client_id = my_settings.client_id
client_secret = my_settings.client_secret

url = "https://openapi.naver.com/v1/search/book?query=" + urllib.parse.quote("검색할 단어") # JSON 결과

headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}

request = urllib.request.Request(url, headers=headers)

response = urllib.request.urlopen(request)
rescode = response.getcode()
if rescode == 200:
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + str(rescode))


connection = mysql.connector.connect(
    host=my_settings.DATABASES['default']['HOST'],
    user=my_settings.DATABASES['default']['USER'],
    password=my_settings.DATABASES['default']['PASSWORD'],
    database=my_settings.DATABASES['default']['NAME']
)

# 커서 생성
cursor = connection.cursor()

try:
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    # API 요청
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 응답 에러 체크

    # 응답 데이터 가져오기
    data = response.json()

    # 데이터 삽입을 위한 커서 생성
    cursor = connection.cursor()

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
        insert_query = "INSERT INTO book (title, author, publisher, pubdate, discount, isbn, image, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        insert_data = (title, author, publisher, pubdate, discount, isbn, image, url)

        # 쿼리 실행
        cursor.execute(insert_query, insert_data)

    # 변경 사항 커밋
    connection.commit()

    print("데이터를 MySQL에 성공적으로 저장했습니다.")

except requests.exceptions.HTTPError as e:
    print(f"HTTP 오류가 발생했습니다: {e}")

except requests.exceptions.RequestException as e:
    print(f"오류가 발생했습니다: {e}")

finally:
    # 연결 닫기
    if connection.is_connected():
        connection.close()
    # 커서 변수가 정의되었는지 확인 후 닫기
    if 'cursor' in locals() and cursor:
        cursor.close()
