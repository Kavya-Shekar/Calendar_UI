import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="prajwal",
    password="180818",
    database="mydatabase"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM my_schedule")
myresult = mycursor.fetchall()
return(myresult) 