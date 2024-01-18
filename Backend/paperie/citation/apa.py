import mysql.connector
import sys
sys.path.append("#")
import my_settings

# 데이터베이스 연결 설정
connection = mysql.connector.connect(
    host = my_settings.MYSQL_HOST,
    user = my_settings.MYSQL_USER,
    password = my_settings.MYSQL_PASSWORD,
    database = my_settings.MYSQL_DATABASE
)

# 커서 생성
cursor = connection.cursor()

# SQL 쿼리 실행
query = 'SELECT * FROM news'
cursor.execute(query)

# 결과 가져오기
result = cursor.fetchall()

# 데이터 처리 및 출력
for row in result:
    # 각 행의 데이터를 가공하여 원하는 형식으로 출력
    print(f'{row[2]}, ({row[4][:4]}), {row[1]}, {row[3]}')

# 연결 및 커서 닫기
cursor.close()
connection.close()
