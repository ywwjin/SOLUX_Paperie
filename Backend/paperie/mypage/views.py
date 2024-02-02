from django.http import JsonResponse
from django.http import HttpResponse
from my_settings import DATABASES
import mysql.connector
import datetime
import sys
sys.path.append(r"C:\Users\한지수\Documents\GitHub\한지수\SOLUX_Paperie(4)\Backend\paperie")
from django.db import connection
import json

def mypage_save(request):
    if request.method == 'POST':
        # POST로 전달된 데이터 받기
        title = request.POST.get('title')
        content = request.POST.getlist('content')
        type = request.POST.get('type')
        ref = request.POST.get('ref')

        # 데이터베이스 연결 설정
        connection = mysql.connector.connect(
            host=DATABASES['default']['HOST'],
            user=DATABASES['default']['USER'],
            password=DATABASES['default']['PASSWORD'],
            database=DATABASES['default']['NAME']
        )
        cursor = connection.cursor()

        try:
            # 쿼리와 데이터 준비
            insert_query = "INSERT INTO result (title, content, ref, type, date) VALUES (%s, %s, %s, %s, %s)"
            insert_data = (title, ', '.join(content), ref, type, datetime.datetime.now())

            # 데이터베이스에 데이터 저장
            with connection.cursor() as cursor:
                cursor.execute(insert_query, insert_data)
            connection.commit()

            # 저장 성공 메시지 반환
            return HttpResponse("데이터 저장이 완료되었습니다.")

        except Exception as e:
            # 저장 실패 메시지 반환
            return HttpResponse(f"데이터 저장 중 오류가 발생했습니다: {str(e)}")

        finally:
            # 연결 종료
            connection.close()

    else:
        return HttpResponse("잘못된 요청입니다.")


def mypage_all(request):

    if request.method == 'GET':
        # 데이터베이스 연결 설정
        cursor = connection.cursor()

        try:
            # 쿼리 실행
            select_query = "SELECT * FROM result"
            cursor.execute(select_query)

            # 조회 결과 가져오기
            results = cursor.fetchall()

            # 결과를 JSON 형식으로 변환하여 반환
            result_list = []
            for row in results:
                result = {
                    'Title': row[1],
                    'Content': row[2],
                    'Ref': row[3],
                    'Type': row[4],
                    'Date': str(row[5])
                }
                result_list.append(result)

            return HttpResponse(json.dumps(result_list), content_type='application/json')

        except Exception as e:
            # 조회 실패 메시지 반환
            return HttpResponse(f"데이터 조회 중 오류가 발생했습니다: {str(e)}")

    else:
        return HttpResponse("잘못된 요청입니다.")