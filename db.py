import mysql.connector
from dotenv import load_dotenv
import os
import time


load_dotenv()

cleardb_str = "mysql://bde8974ff6848a:f82355c4@us-cdbr-east-06.cleardb.net/heroku_03c2a5e7c8a7f77?reconnect=true"

db=mysql.connector.connect(
    host="us-cdbr-east-06.cleardb.net",
    user="bde8974ff6848a",
    passwd="f82355c4",
    database="heroku_03c2a5e7c8a7f77"
    )

mycursor=db.cursor(buffered=True)

# print(mycursor.execute("Show tables;"))

def create_hider(hider_name):
    mycursor.execute(f"CREATE TABLE {hider_name} (name VARCHAR(100),found VARCHAR(100),image_link VARCHAR(100))")


# create_hider("Hiders")


def insert_user(name,found,image_link):
    # mycursor.execute("INSERT INTO Flask_Profile_Info (author,gender,age,job,location) VALUES (%s,%s%s,%s,%s)", ("iphone 69+","Dsams"))
    # mycursor.execute("INSERT INTO Post_Table (author,post_date,post) VALUES (%s,%s,%s)", ("dartsams","Sat Jun 12 14:13:45 2021","i hate life"))
    mycursor.execute("INSERT INTO Hiders (name,found,image_link) VALUES (%s,%s,%s)",(name,found,image_link))
    db.commit()

# insert_user("Maya","Not yet","Image")

def show_entries(table_name):
    user=[]
    mycursor.execute(f"SELECT * FROM {table_name}")
    for i in mycursor:
        # print(i)
        user.append(i)
        # return i
    return user

x = show_entries('Hiders')
print(x)
