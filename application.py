# schedulerdao import
from dao import schedulerdao
from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("trialCalendar.html")


@app.route("/scheduler",methods=["GET","POST","PUT","DELETE"])
def scheduler():
    
    #GET method to render all events
    if request.method == 'GET':
        start = request.args.get('start')
        end = request.args.get('end')
        return schedulerdao.getScheduler({'start':start , 'end' : end})

    #POST method to add events to database
    if request.method == 'POST':
        print("request form", request.form)
        start = request.form['start']
        end = request.form['end']
        title = request.form['title']
        schedule = {'title' : title, 'start' : start, 'end' : end}
        return  schedulerdao.setScheduler(schedule)

    #DELETE method to remove events from the database 
    if request.method == 'DELETE':
        title = request.form['title']
        return  schedulerdao.delScheduler(title)

    #PUT method to modify events in the database
    if request.method == 'PUT':
        schedule = request.form
        return schedulerdao.putScheduler(schedule)

if __name__ =='__main__':
    app.run(debug=True)
