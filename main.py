from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_socketio import (
    SocketIO,
    emit,
    send,
    join_room,
    leave_room,
)  # replaces post requests
from flaskext.mysql import MySQL #allows flask and mysql connection
import os
participants_names = ["Maya","Dart"]

participants_data = {
    "Maya":{
        "name":"Maya",
        "status":"active"
    },
    "Dart":{
        "name":"Dart",
        "status":"active"
    }
}

app = Flask(__name__)
app.config["SECRET_KEY"] = "hello" 
socketio = SocketIO(app)  # init the socket connection

mysql = MySQL()  # to connect flask to mysql
cleardb_str = "mysql://bde8974ff6848a:f82355c4@us-cdbr-east-06.cleardb.net/heroku_03c2a5e7c8a7f77?reconnect=true"
app.config["MYSQL_DATABASE_HOST"] = "us-cdbr-east-06.cleardb.net"
app.config["MYSQL_DATABASE_USER"] = "bde8974ff6848a"
app.config["MYSQL_DATABASE_PASSWORD"] = "f82355c4"
app.config["MYSQL_DATABASE_DB"] = "heroku_03c2a5e7c8a7f77"
mysql.init_app(app)  # init the flask  to mysql connection

conn=mysql.connect()
mycursor=conn.cursor()

def create_hider(hider_name):
    mycursor.execute(f"CREATE TABLE {hider_name} (name VARCHAR(100),found VARCHAR(100),image_link VARCHAR(100))")


# create_hider("Hiders")


def insert_user(name,found="Not Yet",image_link="default link"):
    # mycursor.execute("INSERT INTO Flask_Profile_Info (author,gender,age,job,location) VALUES (%s,%s%s,%s,%s)", ("iphone 69+","Dsams"))
    # mycursor.execute("INSERT INTO Post_Table (author,post_date,post) VALUES (%s,%s,%s)", ("dartsams","Sat Jun 12 14:13:45 2021","i hate life"))
    mycursor.execute("INSERT INTO Hiders (name,found,image_link) VALUES (%s,%s,%s)",(name,found,image_link))
    conn.commit()

# insert_user("Maya","Not yet","Image")

def show_entries(table_name):
    user=[]
    mycursor.execute(f"SELECT * FROM {table_name}")
    for i in mycursor:
        print(i)
        user.append(i)
        # return i
    return user

# show_entries('Hiders')

@app.route("/")
def index():

    data = {
        "participants_data":participants_data,
        "participants_names":participants_names,
        # "participants":[]
    }
    return render_template("index.html",data=data)

@socketio.on("new-participant")
def handle_message(data):
    print(data)
    insert_user(data["name"])

@socketio.on("refresh")
def handle_message(msg):
    hider_lst = show_entries('Hiders')
    print(hider_lst)
    data = {
        "updated_list":hider_lst
    }
    emit("after-refresh",data,broadcast=True)



if __name__ == "__main__":
    socketio.run(app,debug=True,port=8000)

