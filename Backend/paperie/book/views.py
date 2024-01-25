import os
import sys
import urllib.request
import json
import mysql.connector
import datetime
import requests
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import my_settings

sys.path.append(r"C:\Users\한지수\Documents\GitHub\한지수\SOLUX_Paperie(4)\Backend\paperie")

#책 검색 함수
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


#DB에서 제목과 일치하는 정보 가져오는 함수
def get_book_database(selected_title, info_type):
    # MySQL 연결
    connection = mysql.connector.connect(
        host=my_settings.DATABASES['default']['HOST'],
        user=my_settings.DATABASES['default']['USER'],
        password=my_settings.DATABASES['default']['PASSWORD'],
        database=my_settings.DATABASES['default']['NAME']
    )
    cursor = connection.cursor()

    # MySQL에서 선택한 도서 정보 가져오기
    select_query = f"SELECT author, pubdate, title, publisher FROM book WHERE title = '{selected_title}'"
    cursor.execute(select_query)
    books = cursor.fetchall()

    book_info_apa = []
    book_info_mla = []
    book_info_chi = []
    book_info_van = []
    for book in books:
        author = book[0]
        pubdate = str(book[1])[:4]
        title = book[2]
        publisher = book[3]

        rearranged_book_apa = f"{author}. ({pubdate}). {title}. {publisher}."
        rearranged_book_mla = f"{author}. {title}. {publisher}, {pubdate}."
        rearranged_book_chi = f"{author}. {title}. {publisher}, {pubdate}."
        rearranged_book_van = f"{author}. {title}. {publisher}; {pubdate}."

        book_info_apa.append(rearranged_book_apa)
        book_info_mla.append(rearranged_book_mla)
        book_info_chi.append(rearranged_book_chi)
        book_info_van.append(rearranged_book_van)

    # MySQL 연결 종료
    cursor.close()
    connection.close()

    if info_type == 'apa':
        return book_info_apa
    elif info_type == 'mla':
        return book_info_mla
    elif info_type == 'chi':
        return book_info_chi
    elif info_type == 'van':
        return book_info_van
    else:
        return None


#APA 함수
def apa_books(request):
    selected_title = request.GET.get('selected_title')  

    book_info_apa = get_book_database(selected_title, 'apa')

    if not book_info_apa:
        return HttpResponse("도서 정보를 찾을 수 없습니다.", status=404) 

    return HttpResponse(json.dumps(book_info_apa), content_type="application/json")


#MLA 함수
def mla_books(request):
    selected_title = request.GET.get('selected_title')  

    book_info_mla = get_book_database(selected_title, 'mla')

    if not book_info_mla:
        return HttpResponse("도서 정보를 찾을 수 없습니다.", status=404) 

    return HttpResponse(json.dumps(book_info_mla), content_type="application/json")


#CHICAGO 함수
def chi_books(request):
    selected_title = request.GET.get('selected_title')  

    book_info_chi = get_book_database(selected_title, 'chi')

    if not book_info_chi:
        return HttpResponse("도서 정보를 찾을 수 없습니다.", status=404) 

    return HttpResponse(json.dumps(book_info_chi), content_type="application/json")


#VANCUVER 함수
def van_books(request):
    selected_title = request.GET.get('selected_title')  

    book_info_van = get_book_database(selected_title, 'van')

    if not book_info_van:
        return HttpResponse("도서 정보를 찾을 수 없습니다.", status=404) 

    return HttpResponse(json.dumps(book_info_van), content_type="application/json")

