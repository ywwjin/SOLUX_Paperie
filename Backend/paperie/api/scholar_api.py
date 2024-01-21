import requests
import mysql.connector
import sys
sys.path.append("C:/Users/김유진/OneDrive/문서/GitHub/SOLUX_Paperie/Backend/paperie/paperie")
import my_settings

connection = mysql.connector.connect(
    host = my_settings.MYSQL_HOST,
    user = my_settings.MYSQL_USER,
    password = my_settings.MYSQL_PASSWORD,
    database = my_settings.MYSQL_DATABASE
    )

cursor = connection.cursor()

def search_crossref(query, num_results=10):
    url = ('https://api.crossref.org/works?'
           f'query={query}'
           f'&rows={num_results}'
           '&filter=type:journal-article')
    response = requests.get(url)



    if response.status_code == 200:
        data = response.json()
        items = data.get('message', {}).get('items', [])

        for item in items:
            # 필요한 데이터 추가
            authors = ', '.join(author.get('given', '') + ' ' + author.get('family', '') for author in item.get('author', []))
            title = ''.join(item.get('title', ''))
            journal_title = item.get('container-title', [''])[0]
            volume = item.get('volume', '')
            issue = item.get('issue', '')
            year = item.get('published-print', {}).get('date-parts', [['']])[0][0]
            page = item.get('page', '')
            

            #mysql에 데이터 삽입
            try:
                # 데이터 삽입 쿼리
                insert_query = "INSERT INTO scholar (authors, title, journal_title, volume, issue, year, page) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                data = (authors, title, journal_title, volume, issue, year, page)
                print(data)

                # 데이터를 풀어서 전달
                cursor.execute(insert_query, data)

                # 변경 사항 커밋
                connection.commit()
                print("Data saved to MySQL successfully.")

            except mysql.connector.Error as e:
                print(f'Error inserting data into MySQL: {e}')

            finally:
                if 'cursor' in locals():
                    cursor.close()

        
        #mysql 연결 종료
        connection.close()

    else:
        print(f'Error: {response.status_code}')
        print(response.text)


def insert_data_to_mysql(connection, data):
    try:
        

        # 데이터 삽입 쿼리
        insert_query = "INSERT INTO scholar (authors, title, journal_title, volume, issue, year, page) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        # 데이터를 풀어서 전달
        cursor.execute(insert_query, data)

        # 변경 사항 커밋
        connection.commit()
        print("Data saved to MySQL successfully.")

    except mysql.connector.Error as e:
        print(f'Error inserting data into MySQL: {e}')

    finally:
        if 'cursor' in locals():
            cursor.close()


# 위에서 정의한 작업 유형에 해당하는 결과만 가져오기
#query ='검색할 키워드 입력'
search_crossref(query ='Quantum computing', num_results=10)