from django.http import JsonResponse
from django.http import HttpResponse
from my_settings import DATABASES
import mysql.connector
import sys
sys.path.append(r"C:\Users\한지수\Documents\GitHub\한지수\SOLUX_Paperie(4)\Backend\paperie")

def mypage_get(request):
    if request.method == 'GET':
        title = request.GET.get('title')
        ref = request.GET.get('ref')

        # MySQL 연결 설정
        connection = mysql.connector.connect(
            host=DATABASES['default']['HOST'],
            user=DATABASES['default']['USER'],
            password=DATABASES['default']['PASSWORD'],
            database=DATABASES['default']['NAME']
        )
        cursor = connection.cursor()

        # 쿼리 생성 및 실행
        query = "SELECT * FROM result WHERE title = %s AND ref = %s"
        cursor.execute(query, (title, ref))

        # 결과 가져오기 및 딕셔너리 형태로 변환
        result = cursor.fetchall()
        result_without_id = [{
            'type': item[1],
            'ref': item[2],
            'content': item[3],
            'title': item[4],
            'date': item[5]
        } for item in result]

        # 연결 종료
        cursor.close()
        connection.close()

        # JSON 형식으로 응답 반환
        return JsonResponse(result_without_id, safe=False)

    else:
        return HttpResponse('잘못된 요청입니다.', status=400)


def mypage_books(request):
    if request.method == 'GET':
        try:
            connection = mysql.connector.connect(
                host=DATABASES['default']['HOST'],
                user=DATABASES['default']['USER'],
                password=DATABASES['default']['PASSWORD'],
                database=DATABASES['default']['NAME']
            )
            cursor = connection.cursor()

            # '책' 타입인 항목만 가져오는 쿼리문
            query = "SELECT * FROM result WHERE type='책'"

            # 쿼리 실행
            cursor.execute(query)

            # 결과 가져오기
            result = cursor.fetchall()

            # '책' 타입인 항목만 필터링하여 반환
            result_filtered = [{
                'type': item[1],
                'ref': item[2],
                'content': item[3],
                'title': item[4],
                'date': item[5]
            } for item in result if item[1] == '책']

            cursor.close()
            connection.close()

            return JsonResponse(result_filtered, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return HttpResponse('잘못된 요청입니다.', status=400)


def mypage_news(request):
    if request.method == 'GET':
        try:
            connection = mysql.connector.connect(
                host=DATABASES['default']['HOST'],
                user=DATABASES['default']['USER'],
                password=DATABASES['default']['PASSWORD'],
                database=DATABASES['default']['NAME']
            )
            cursor = connection.cursor()

            # '뉴스' 타입인 항목만 가져오는 쿼리문
            query = "SELECT * FROM result WHERE type='뉴스'"

            # 쿼리 실행
            cursor.execute(query)

            # 결과 가져오기
            result = cursor.fetchall()

            # '뉴스' 타입인 항목만 필터링하여 반환
            result_filtered = [{
                'type': item[1],
                'ref': item[2],
                'content': item[3],
                'title': item[4],
                'date': item[5]
            } for item in result if item[1] == '뉴스']

            cursor.close()
            connection.close()

            return JsonResponse(result_filtered, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return HttpResponse('잘못된 요청입니다.', status=400)
    

def mypage_scholars(request):
    if request.method == 'GET':
        try:
            connection = mysql.connector.connect(
                host=DATABASES['default']['HOST'],
                user=DATABASES['default']['USER'],
                password=DATABASES['default']['PASSWORD'],
                database=DATABASES['default']['NAME']
            )
            cursor = connection.cursor()

            # '논문' 타입인 항목만 가져오는 쿼리문
            query = "SELECT * FROM result WHERE type='논문'"

            # 쿼리 실행
            cursor.execute(query)

            # 결과 가져오기
            result = cursor.fetchall()

            # '논문' 타입인 항목만 필터링하여 반환
            result_filtered = [{
                'type': item[1],
                'ref': item[2],
                'content': item[3],
                'title': item[4],
                'date': item[5]
            } for item in result if item[1] == '논문']

            cursor.close()
            connection.close()

            return JsonResponse(result_filtered, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return HttpResponse('잘못된 요청입니다.', status=400)

