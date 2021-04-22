
import json
import pymysql
import os
from email.message import EmailMessage
import smtplib
  

def getConnection():
    return pymysql.connect(host='localhost', user='prajwal', password='180818',
                           db='mydatabase', charset='utf8')

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def sql_template(type, sql, params=None):
    # Connection
    connetion = getConnection()
    try:
        #insert, update, delete
        if type == 3 :
            with connetion.cursor() as cursor :
                
                rows = cursor.execute(sql, params)
                # commit
                connetion.commit()
                return rows
        else :
            
            with connetion.cursor(pymysql.cursors.DictCursor) as cursor :
                
                cursor.execute(sql, params)
                
                if type == 1 :
                    return cursor.fetchall()
                elif type == 2 :
                    return cursor.fetchone()
    finally:
        
        connetion.close()


def getScheduler(searchDate):
    if not parameter_checker(searchDate) :
        return json.dumps({})
    sql = "select id, title, start, end"
    params = ('Y', searchDate['start'], searchDate['end'])
    
    return json.dumps(sql_template(1, sql, params), default=date_handler);


def setScheduler(schedule):
    print('Functoin called')
    if not parameter_checker(schedule) :
        print('Found the error')
        return json.dumps({'rows' : 0})

    else :

        print('Stuck with the error')
        json_file = open(os.path.dirname(__file__) + '/../static/loadtest.json', 'r')
        data = json.load(json_file)
        
        new_event = {
            "title": schedule['title'],
            "start": schedule['start'].replace('/', '-'),
            "end": schedule['end'].replace('/', '-'),
            "color": "green"
        }
        json_file.close()
        
        f = open(os.path.dirname(__file__) + '/../static/loadtest.json', 'w')
        data.append(new_event)
        json.dump(data, f)
        f.close()
        print('Added event to database')

        # invitees = schedule['invitees']
        # if invitees != '':
        #     invitees = invitees.split(";")            
            
        #     s = smtplib.SMTP_SSL('smtp.gmail.com')
        #     s.login("ooadcalendartest@gmail.com", "ooadcool")
            
        #     msg = EmailMessage()
        #     msg['Subject'] = f'Event invitation'
        #     msg['To'] = ', '.join(invitees)
        #     msg['From'] = "ooadcalendartest@gmail.com"
        #     mail_body = r"You have been invited to {} at {}".format( schedule["title"], schedule["start"])
        #     msg.set_content(mail_body)
        #     s.send_message(msg)
        #     print('Send mail!')

        #     s.quit()



        sql = "INSERT INTO my_schedule(title, start, end) VALUES (%s, %s, %s)"
        params = (schedule['title'], schedule['start'], schedule['end'])
        return json.dumps({'rows' : sql_template(3, sql, params)})


def delScheduler(title):
    if not parameter_checker(title) :
        return json.dumps({'rows' : 0})

    else :        
        json_data = json.load(open(os.path.dirname(__file__) + '/../static/loadtest.json'))
        for i in range(len(json_data)):
            if json_data[i]['title'] == title:
                json_data.pop(i)
                break

        f = open(os.path.dirname(__file__) + '/../static/loadtest.json', 'w')
        json.dump(json_data, f)
        f.close()

        sql = "DELETE FROM my_schedule WHERE title = %s;"
        params = (title)
        print(title)
        return json.dumps({'rows' : sql_template(1, sql, params)})

def putScheduler(schedule):
    if not parameter_checker(schedule) :
        return json.dumps({'rows' : 0})

    else :
        title  = schedule['newTitle']
        start_date = schedule['newStart']
        end_date = schedule['newEnd']
        json_data = json.load(open(os.path.dirname(__file__) + '/../static/loadtest.json'))
        for i in range(len(json_data)):
            print(title)
            if json_data[i]['title'] == title:
                json_data[i]["start"] = start_date.replace('/', '-')
                json_data[i]["end"] = end_date.replace('/', '-')
                print('found!!\n\n\n\n\n')
                break


        f = open(os.path.dirname(__file__) + '/../static/loadtest.json', 'w')
        json.dump(json_data, f)
        f.close()

        sql = "UPDATE my_schedule SET start = %s, end = %s WHERE title = %s;"
        params = (schedule['newStart'], schedule['newEnd'], schedule['newTitle'])
        return json.dumps({'rows' : sql_template(3, sql, params)})

def parameter_checker(params):
    return True

    if not bool(params):
        return False
        
    elif hasattr(params,'strip') and not bool(params.strip()):
            return False
            
    elif hasattr(params,'values'):
        for value in params.values() :
            if not parameter_checker(value) :
                return False
        return True
    else:
        return True
