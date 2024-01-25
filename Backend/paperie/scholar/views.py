import requests
import mysql.connector
from django.conf import settings
import sys
from my_settings import DATABASES
import urllib.parse
from django.http import HttpResponse  # HttpResponse import 추가

sys.path.append(r"C:\Users\한지수\Documents\GitHub\한지수\SOLUX_Paperie(4)\Backend\paperie")

def search_scholar(request):
    # query, num_results, filter 설정
    query = request.GET.get('query')  # 검색어 가져오기
    # URL 생성
    base_url = 'https://api.crossref.org/works?'
    query_param = urllib.parse.quote(query.encode("utf-8"))
    url = f'{base_url}query={query_param}'

    # 요청 보내기
    response = requests.get(url)

    # MySQL 연결
    connection = mysql.connector.connect(
        host=DATABASES['default']['HOST'],
        user=DATABASES['default']['USER'],
        password=DATABASES['default']['PASSWORD'],
        database=DATABASES['default']['NAME']
    )
   
    cursor = connection.cursor()

    if response.status_code == 200:
        data = response.json()
        items = data.get('message', {}).get('items', [])

        for item in items:
            authors = ', '.join(author.get('given', '') + ' ' + author.get('family', '') for author in item.get('author', []))
            title = ''.join(item.get('title', ''))
            journal_title = item.get('container-title', [''])[0]
            volume = item.get('volume', '')
            issue = item.get('issue', '')
            year = item.get('published-print', {}).get('date-parts', [['']])[0][0]
            page = item.get('page', '')

            # MySQL에 데이터 삽입
            try:
                insert_query = "INSERT INTO scholar (authors, title, journal_title, volume, issue, year, page) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                data = (authors, title, journal_title, volume, issue, year, page)
                
                cursor.execute(insert_query, data)
                connection.commit()
                print("Data saved to MySQL successfully.")

            except mysql.connector.Error as e:
                print(f'Error inserting data into MySQL: {e}')

        # MySQL 연결 종료
        cursor.close()
        connection.close()

        return HttpResponse("Data saved to MySQL successfully.")  # 데이터 저장 성공 시 응답 반환

    else:
        print(f'Error: {response.status_code}')
        print(response.text)
        return HttpResponse(f'Error: {response.status_code}')  # 오류 발생 시 응답 반환
