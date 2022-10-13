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
app.config["MYSQL_DATABASE_HOST"] = "us-cdbr-east-04.cleardb.com"
app.config["MYSQL_DATABASE_USER"] = "bcc2ec4fcecbe5"
app.config["MYSQL_DATABASE_PASSWORD"] = "Dartagnan19@"
app.config["MYSQL_DATABASE_DB"] = "heroku_d10e4ce632a9633"
mysql.init_app(app)  # init the flask  to mysql connection

conn=mysql.connect()
mycursor=conn.cursor()

def create_hider(hider_name):
    mycursor.execute(f"CREATE TABLE {hider_name} (name VARCHAR(100),found VARCHAR(100),image_link VARCHAR(100))")

@app.route("/")
def index():
    create_hider("Maya")
    data = {
        "participants_data":participants_data,
        "participants_names":participants_names
    }
    return render_template("index.html",data=data)


if __name__ == "__main__":
    socketio.run(app,debug=True,port=8000)

