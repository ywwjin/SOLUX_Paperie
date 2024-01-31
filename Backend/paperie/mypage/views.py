from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from my_settings import DATABASES
import mysql.connector

def mypage_get(request):
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

    # title과 ref가 모두 일치하는 컬럼을 찾는 쿼리문
    query = f"SELECT * FROM result WHERE title='{title}' AND ref='{ref}'"

    # 쿼리 실행
    cursor.execute(query)

    # 결과 가져오기
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

    return JsonResponse(result_without_id, safe=False)

def mypage(request):
    return