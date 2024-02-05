import requests
import json
import mysql.connector
from django.conf import settings
import sys
from my_settings import DATABASES
import urllib.parse
from django.http import HttpResponse  # HttpResponse import 추가
from mysql.connector import Error
import datetime
from django.http import JsonResponse

sys.path.append(r"C:/Users/김유진/OneDrive/문서/GitHub/SOLUX_Paperie/Backend/paperie/paperie")

def search_scholars(request):
    # query, num_results, filter 설정
    query = request.GET.get('query')  # 검색어 가져오기
    # URL 생성
    base_url = 'https://api.crossref.org/works?'
    query_param = urllib.parse.quote(query.encode("utf-8"))
    url = f'{base_url}query={query_param}&rows=10'

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

        output = []

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


            scholar_info = {
                    'title': title,
                    'author': authors,
                    'year': year
                }
            output.append(scholar_info) 

        # MySQL 연결 종료
        cursor.close()
        connection.close()

        return HttpResponse(json.dumps(output), content_type='application/json')

    else:
        print(f'Error: {response.status_code}')
        print(response.text)
        return HttpResponse(f'Error: {response.status_code}')  # 오류 발생 시 응답 반환

#참고문헌 프린트
def get_scholar_database(selected_title, info_type):
    
    # MySQL 연결
    connection = mysql.connector.connect(
        host=DATABASES['default']['HOST'],
        user=DATABASES['default']['USER'],
        password=DATABASES['default']['PASSWORD'],
        database=DATABASES['default']['NAME']
    )

    #mysql 데이터 조회
    cursor = connection.cursor()

    try:
        
        #논문 제목 확인을 위한 쿼리
        select_query = "SELECT * FROM scholar WHERE title = %s"
        cursor.execute(select_query, (selected_title,))
        scholars = cursor.fetchall()

        #논문 존재하는 경우 
        scholar_info_apa = []
        scholar_info_mla = []
        scholar_info_chi = []
        scholar_info_van = []

        # 기본값 정의
        default_author = '저자명'
        default_pubdate = '발행년도'
        default_title = '논문명'
        default_journal_title = '저널명'
        default_volume = '권'
        default_issue = '호'
        default_page = '페이지'

        for scholar in scholars:
            author = scholar[1] if scholar[1] else default_author
            pubdate = scholar[6] if scholar[6] else default_pubdate
            title = scholar[2] if scholar[2] else default_title
            journal_title = scholar[3] if scholar[3] else default_journal_title
            volume = scholar[4] if scholar[4] else default_volume
            issue = scholar[5] if scholar[5] else default_issue
            page = scholar[7] if scholar[7] else default_page

            # 저자명 (발행년도). 논문명. 저널명, 권(호), 페이지. doi
            rearranged_scholar_apa = f'{author}. ({pubdate}). {journal_title}, {volume}({issue}), {page}.'
            rearranged_scholar_mla = f'{author}. "{title}". {journal_title}, vol.{volume}, no.{issue}, {pubdate}, pp.{page}.'
            rearranged_scholar_chi = f'{author}. "{title}". {journal_title} {volume}, no.{issue}, ({pubdate}):{page}.'
            rearranged_scholar_van = f'{author}. {title}. {journal_title}. {pubdate}; {volume}({issue}): {page}.'
    

            scholar_info_apa.append(rearranged_scholar_apa)
            scholar_info_mla.append(rearranged_scholar_mla)
            scholar_info_chi.append(rearranged_scholar_chi)
            scholar_info_van.append(rearranged_scholar_van)

        # MySQL 연결 종료
        cursor.close()
        connection.close()

        if info_type == 'apa':
            return scholar_info_apa
        elif info_type == 'mla':
            return scholar_info_mla
        elif info_type == 'chi':
            return scholar_info_chi
        elif info_type == 'van':
            return scholar_info_van
        else:
            return None

    except mysql.connector.Error as e:
        print(f'Error checking and printing paper: {e}')

    finally:
        cursor.close()


# 데이터베이스 연결 및 데이터 삽입 함수
def insert_data_to_database(title, content, ref):
    try:
        connection = mysql.connector.connect(
            host=DATABASES['default']['HOST'],
            user=DATABASES['default']['USER'],
            password=DATABASES['default']['PASSWORD'],
            database=DATABASES['default']['NAME']
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # MySQL에 데이터 삽입하는 쿼리
            insert_query = "INSERT INTO result (title, content, ref, type, date) VALUES (%s, %s, %s, %s, %s)"
            insert_data = (title, ', '.join(content), ref, "논문", datetime.datetime.now())

            # 쿼리 실행
            cursor.execute(insert_query, insert_data)
            connection.commit()

            # MySQL 연결 종료
            cursor.close()
            connection.close()

    except Error as e:
        print("MySQL 연결 오류:", e)
        # 오류 처리를 원하는 방식으로 수정해주세요 

# APA 함수
def apa_scholars(request):
    selected_title = request.GET.get('selected_title')  

    scholar_info_apa = get_scholar_database(selected_title, 'apa')

    if not scholar_info_apa:
        return HttpResponse("논문 정보를 찾을 수 없습니다.", status=404)

    insert_data_to_database(selected_title, scholar_info_apa, "APA")

    return HttpResponse(json.dumps(scholar_info_apa[0]), content_type="application/json")

# MLA 함수
def mla_scholars(request):
    selected_title = request.GET.get('selected_title')  

    scholar_info_mla = get_scholar_database(selected_title, 'mla')

    if not scholar_info_mla:
        return HttpResponse("논문 정보를 찾을 수 없습니다.", status=404)

    insert_data_to_database(selected_title, scholar_info_mla, "MLA")

    return HttpResponse(json.dumps(scholar_info_mla[0]), content_type="application/json")

# CHICAGO 함수
def chi_scholars(request):
    selected_title = request.GET.get('selected_title')  

    scholar_info_chi = get_scholar_database(selected_title, 'chi')

    if not scholar_info_chi:
        return HttpResponse("논문 정보를 찾을 수 없습니다.", status=404) 

    insert_data_to_database(selected_title, scholar_info_chi, "CHI")

    return HttpResponse(json.dumps(scholar_info_chi[0]), content_type="application/json")

# VANCUVER 함수
def van_scholars(request):
    selected_title = request.GET.get('selected_title')  

    scholar_info_van = get_scholar_database(selected_title, 'van')

    if not scholar_info_van:
        return HttpResponse("논문 정보를 찾을 수 없습니다.", status=404)

    insert_data_to_database(selected_title, scholar_info_van, "VAN")

    return HttpResponse(json.dumps(scholar_info_van[0]), content_type="application/json")