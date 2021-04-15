# -- coding: utf-8 --
#처리된 데이터를 json형식으로 리턴해주기위해 사용
import json
#python mysql 연결 드라이버
import pymysql
import os

#db연결을 담당할 함스
def getConnection():
    return pymysql.connect(host='localhost', user='prajwal', password='180818',
                           db='mydatabase', charset='utf8')


#select한 데이터중 mysql datetime형식의 값을 fullCalendar에서 처리할수 있도록 포멧 변경
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

#sql 중복 부분 리팩토링
def sql_template(type, sql, params=None):
    # Connection 연결
    connetion = getConnection()
    try:
        #insert, update, delete 사용
        if type == 3 :
            with connetion.cursor() as cursor :
                # 데이터 입력
                rows = cursor.execute(sql, params)
                # commit
                connetion.commit()
                return rows
        else :
            # 1 = fetchall() 2 = fetchone()
            with connetion.cursor(pymysql.cursors.DictCursor) as cursor :
                # SQL 처리
                cursor.execute(sql, params)
                # 처리된 data 가져옴
                if type == 1 :
                    return cursor.fetchall()
                elif type == 2 :
                    return cursor.fetchone()
    finally:
        # Connection 닫기
        connetion.close()

#등록된 schedule을 가져옴
def getScheduler(searchDate):
    if not parameter_checker(searchDate) :
        return json.dumps({})
    sql = "select id, title, start, end"
    params = ('Y', searchDate['start'], searchDate['end'])
    #처리된 데이터를 json으로 변경 datetime처리를 위해 date_handler지정
    return json.dumps(sql_template(1, sql, params), default=date_handler);

#넘어온 schedule을 등록
def setScheduler(schedule):

    #넘어온 데이터중 빈값이 있으면 0 리턴
    if not parameter_checker(schedule) :
        return json.dumps({'rows' : 0})
    else :
        json_file = open(os.path.dirname(__file__) + '/../static/loadtest.json', 'r')
        data = json.load(json_file)
        id = len(data)+1
        new_event = {
            "title": schedule['title'],
            "start": schedule['start'],
            "end": schedule['end']
        }
        json_file.close()
        
        f = open(os.path.dirname(__file__) + '/../static/loadtest.json', 'w')
        data.append(new_event)
        json.dump(data, f)
        f.close()

        sql = "INSERT INTO my_schedule(title, start, end) VALUES (%s, %s, %s)"
        params = (schedule['title'], schedule['start'], schedule['end'])
        return json.dumps({'rows' : sql_template(3, sql, params)})

# schedule 삭제
def delScheduler(title):
    #넘어온 데이터중 빈값이 있으면 0 리턴
    if not parameter_checker(title) :
        return json.dumps({'rows' : 0})
    else :
        
        sql = "DELETE FROM my_schedule WHERE title = %s"
        params = (title)
        return json.dumps({'rows' : sql_template(3, sql, params)})

#넘어온 schedule id에 해당하는 schedule을 수정
def putScheduler(schedule):
    #넘어온 데이터중 빈값이 있으면 0 리턴
    if not parameter_checker(schedule) :
        return json.dumps({'rows' : 0})
    else :
        json_file = open(os.path.dirname(__file__) + '/../static/loadtest.json', 'r')
        data = json.load(json_file)
        id = len(data)+1
        new_event = {
            "title": schedule['title'],
            "start": schedule['start'],
            "end": schedule['end']
        }
        json_file.close()
        

        sql = "UPDATE my_schedule start = %s, end = %s WHERE title = %s"
        params = (schedule['start'], schedule['end'], schedule['title'])
        return json.dumps({'rows' : sql_template(3, sql, params)})

# parameter 빈값 확인
def parameter_checker(params):
    #0이거나 공백일경우 false
    if not bool(params):
        return False
    #str 이나 unicode일경우 trim 된 문자열이 공백인지 확인
    elif hasattr(params,'strip') and not bool(params.strip()):
            return False
    # Dictoionary형식의 타입 체크
    elif hasattr(params,'values'):
        for value in params.values() :
            if not parameter_checker(value) :
                return False
        return True
    else:
        return True
