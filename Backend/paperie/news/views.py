from django.http import JsonResponse
import requests
import urllib
import json
from urllib.parse import quote_plus
import mysql.connector
from my_settings import NEWS_API_KEY, DATABASES
import sys
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
sys.path.append(r"C:/Users/김유진/OneDrive/문서/GitHub/SOLUX_Paperie/Backend/paperie/paperie")
import my_settings

def search_news(request):

    query = request.GET.get('q','')

    url = ('https://newsapi.org/v2/everything?'
           f'q={quote_plus(query)}&'
           'sortBy=popularity&'
           f'apiKey={NEWS_API_KEY}&'
           'pageSize=10')

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



#DB에서 제목과 일치하는 정보 가져오는 함수
def get_news_database(selected_title, info_type):
    # MySQL 연결
    connection = mysql.connector.connect(
        host=my_settings.DATABASES['default']['HOST'],
        user=my_settings.DATABASES['default']['USER'],
        password=my_settings.DATABASES['default']['PASSWORD'],
        database=my_settings.DATABASES['default']['NAME']
    )
    cursor = connection.cursor()

    # MySQL에서 선택한 도서 정보 가져오기
    select_query = "SELECT title, author, url, publish, name FROM news WHERE title = %s"
    cursor.execute(select_query, (selected_title,))

    newss = cursor.fetchall()

    news_info_apa = []
    news_info_mla = []
    news_info_chi = []
    news_info_van = []
    for news in newss:
        title = news[0]
        author = news[1]
        url = news[2]
        publish = news[3]
        name = news[4]

        # publish 변수에서 날짜 부분 추출
        date_str = publish[:10]
        
        # 날짜 형식 변환
        year = date_str[:4]  # 연도
        month = date_str[5:7]  # 월
        day = date_str[8:10]  # 일

        print("date_str:", date_str)
        print("year:", year)
        print("month:", month)
        print("day:", day)

        # 변환된 날짜 다시 할당
        publish = f"{year}년 {int(month)}월 {int(day)}일"

        rearranged_news_apa = f"{title}.[웹사이트]. ({publish}). Retrieved from {url}."
        rearranged_news_mla = f"{author}. \"{title}\". {name}, {publish}, {url}. 접속년도 접속월 접속일"
        rearranged_news_chi = f"\"{title}\". {name}. {publish} 수정, 접속년도 접속월 접속일, {url}."
        rearranged_news_van = f"{author}. \"{title}\". {name}, {publish}.  접속년도 접속월 접속일"

        news_info_apa.append(rearranged_news_apa)
        news_info_mla.append(rearranged_news_mla)
        news_info_chi.append(rearranged_news_chi)
        news_info_van.append(rearranged_news_van)

    # MySQL 연결 종료
    cursor.close()
    connection.close()

    if info_type == 'apa':
        return news_info_apa
    elif info_type == 'mla':
        return news_info_mla
    elif info_type == 'chi':
        return news_info_chi
    elif info_type == 'van':
        return news_info_van
    else:
        return None


#APA 함수
def apa_news(request):
    selected_title = request.GET.get('selected_title')  

    news_info_apa = get_news_database(selected_title, 'apa')

    if not news_info_apa:
        return HttpResponse("뉴스 정보를 찾을 수 없습니다.", status=404) 

    return HttpResponse(json.dumps(news_info_apa[0]), content_type="application/json")


#MLA 함수
def mla_news(request):
    selected_title = request.GET.get('selected_title')  

    news_info_mla = get_news_database(selected_title, 'mla')

    if not news_info_mla:
        return HttpResponse("뉴스 정보를 찾을 수 없습니다.", status=404) 

    return HttpResponse(json.dumps(news_info_mla[0]), content_type="application/json")


#CHICAGO 함수
def chi_news(request):
    selected_title = request.GET.get('selected_title')  

    news_info_chi = get_news_database(selected_title, 'chi')

    if not news_info_chi:
        return HttpResponse("뉴스 정보를 찾을 수 없습니다.", status=404) 

    return HttpResponse(json.dumps(news_info_chi[0]), content_type="application/json")


#VANCUVER 함수
def van_news(request):
    selected_title = request.GET.get('selected_title')  

    news_info_van = get_news_database(selected_title, 'van')

    if not news_info_van:
        return HttpResponse("뉴스 정보를 찾을 수 없습니다.", status=404) 

    return HttpResponse(json.dumps(news_info_van[0]), content_type="application/json")

#참고문헌 옮기기 함수
'''def news_citation_database(title, ):
    try:
        # 새로운 데이터베이스에 데이터 삽입
        insert_query = "INSERT INTO new_news (title, apa_format, mla_format) VALUES (%s, %s, %s)"
        data = (title, apa_format, mla_format)

        new_cursor.execute(insert_query, data)

        # 변경 사항을 커밋
        new_db_connection.commit()

        print(f"News with title '{title}' inserted into the new database successfully.")

    except Exception as e:
        print(f"Error inserting news into the new database: {str(e)}")

    finally:
        # 커넥션 닫기
        new_cursor.close()
        new_db_connection.close()

# APA 및 MLA 형식으로 변환된 뉴스 가져오기
news_info_apa = get_news_database(selected_title, 'apa')
news_info_mla = get_news_database(selected_title, 'mla')

# 새로운 데이터베이스에 데이터 삽입
if news_info_apa and news_info_mla:
    insert_news_to_new_database(selected_title, news_info_apa[0], news_info_mla[0])
else:
    print("뉴스 정보를 찾을 수 없습니다.")'''