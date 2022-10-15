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
from pymongo import MongoClient



app = Flask(__name__)
app.config["SECRET_KEY"] = "hello" 
socketio = SocketIO(app)  # init the socket connection
db_str = "mongodb+srv://DartSams:Dartagnan_19@personal-cluser-db.qavgfkq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(db_str)
mydb = client["Personal_db"] #connects to db but if not found will create it 
table1 = mydb["Hiders"] #connects to table but if not found will create it 


# mysql = MySQL()  # to connect flask to mysql
# cleardb_str = "mysql://bde8974ff6848a:f82355c4@us-cdbr-east-06.cleardb.net/heroku_03c2a5e7c8a7f77?reconnect=true"
# app.config["MYSQL_DATABASE_HOST"] = "us-cdbr-east-06.cleardb.net"
# app.config["MYSQL_DATABASE_USER"] = "bde8974ff6848a"
# app.config["MYSQL_DATABASE_PASSWORD"] = "f82355c4"
# app.config["MYSQL_DATABASE_DB"] = "heroku_03c2a5e7c8a7f77"
# mysql.init_app(app)  # init the flask  to mysql connection

# conn=mysql.connect()
# mycursor=conn.cursor()

# def create_hider(hider_name):
#     mycursor.execute(f"CREATE TABLE {hider_name} (name VARCHAR(100),found VARCHAR(100),image_link VARCHAR(100))")


# def insert_user(name,found="Not Yet",image_link="default link"):
#     mycursor.execute("INSERT INTO Hiders (name,found,image_link) VALUES (%s,%s,%s)",(name,found,image_link))
#     conn.commit()


# def show_entries(table_name):
#     user=[]
#     mycursor.execute(f"SELECT * FROM {table_name}")
#     for i in mycursor:
#         print(i)
#         user.append(i)
#         # return i
#     return user

lst = ["maya","amaya","jaedon","nelson","ola","dart","stronk","sunny","vinny","zaleci"]
print("resetting")
for i in lst:

    data = {
        "name":i.upper(),
        "status":"Not yet",
        "image_link":f"static\pics\{i}.png"
        
    }
    table1.insert_one(data) #inserts into db

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("reset")
def reset(msg):
    lst = ["maya","amaya","jaedon","nelson","ola","dart","stronk","sunny","vinny","zaleci"]
    print("resetting")
    for i in lst:
        for x in table1.find({},{ "name": i.upper()}):
            if x:
                continue
            else:
                data = {
                    "name":i.upper(),
                    "status":"Not yet",
                    "image_link":f"static\pics\{i}.png"
                    
                }
                table1.insert_one(data) #inserts into db


@socketio.on("new-participant")
def handle_message(msg):
    print(msg)
    data = {
        "name":msg["name"],
        "status":"Not yet",
        "image_link":"static\stock.jpg"
        
    }
    table1.insert_one(data) #inserts into db
    # client.close()
    # insert_user(data["name"])

@socketio.on("refresh")
def handle_message(msg):
    print(msg)
    # client = MongoClient(db_str)
    # mydb = client["Personal_db"] #connects to db but if not found will create it 
    # table1 = mydb["Hiders"] #connects to table but if not found will create it 
    # print(table1)
    hider_lst = []
    for x in table1.find({},{"_id":0}):
        print(x)
        if x not in hider_lst:
            hider_lst.append(x)
    print(hider_lst)
    # hider_lst = show_entries('Hiders')
    # print(hider_lst)
    data = {
        "updated_list":hider_lst
    }
    emit("after-refresh",data,broadcast=True)

@socketio.on("change status")
def change_status(msg):
    # client = MongoClient(db_str)
    # mydb = client["Personal_db"] #connects to db but if not found will create it 

    # table1 = mydb["broker"] #connects to table but if not found will create it 
    print(msg)
    print(type(msg["status"]))
    new_status = ""

    myquery = { "name": msg["name"] }

    table1.delete_one(myquery)
    # if msg["status"] != "Found":
    #     new_status = "Found"
    #     print("changing status")

    # else:
    #     new_status = "Not Yet"
    #     print("Resetting")

    # if msg["status"] == "Not yet":
    #     print("found")

    # else:
    #     print("Not Yet")

    # old_data = {
    #     "name":msg["name"],
    # }

    # new_data = {
    #     "$set":{
    #         "status":new_status,
    #     }
    # } # the keyword <$set> is needed to represent that its going to updata the column
    # table1.update_one(old_data,new_data) #takes 2 parameters the 1st finds the entry in db collection then replaces it with the 2nd paramater
    # client.close()
if __name__ == "__main__":
    socketio.run(app,debug=True,port=8000)

