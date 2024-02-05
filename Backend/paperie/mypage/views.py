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
        body = request.body.decode('utf-8')
        data = json.loads(body)

        content = data.get('content')
        ftype = data.get('type')
        ref = data.get('ref')
        date = datetime.datetime.now()  # 현재 날짜 및 시간 가져오기

        # 데이터베이스 연결 설정
        connection = mysql.connector.connect(
            host=DATABASES['default']['HOST'],
            user=DATABASES['default']['USER'],
            password=DATABASES['default']['PASSWORD'],
            database=DATABASES['default']['NAME']
        )
        cursor = connection.cursor()

        # 데이터 저장 쿼리 실행
        insert_query = "INSERT INTO save (s_content, s_type, s_ref, s_date) VALUES (%s, %s, %s, %s)"
        values = (content, ftype, ref, date)  # 날짜 데이터 포함
        cursor.execute(insert_query, values)
        connection.commit()

        # 연결 종료
        cursor.close()
        connection.close()

        return HttpResponse("데이터 저장이 완료되었습니다.")

    else:
        return HttpResponse("잘못된 요청입니다.")


def mypage_all(request):

    if request.method == 'GET':
        # 데이터베이스 연결 설정
        cursor = connection.cursor()

        try:
            # 쿼리 실행
            select_query = "SELECT * FROM save"
            cursor.execute(select_query)

            # 조회 결과 가져오기
            results = cursor.fetchall()

            # 결과를 JSON 형식으로 변환하여 반환
            result_list = []
            for row in results:
                result = {
                    'Content': row[2],
                    'Ref': row[3],
                    'Type': row[1],
                    'Date': str(row[4])
                }
                result_list.append(result)

            return HttpResponse(json.dumps(result_list), content_type='application/json')

        except Exception as e:
            # 조회 실패 메시지 반환
            return HttpResponse(f"데이터 조회 중 오류가 발생했습니다: {str(e)}")

    else:
        return HttpResponse("잘못된 요청입니다.")