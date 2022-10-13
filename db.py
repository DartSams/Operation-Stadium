import dotenv
import os
import random
import json
from pymongo import MongoClient

dotenv.load_dotenv
db_str = "mongodb+srv://DartSams:Dartagnan_19@personal-cluser-db.qavgfkq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(db_str)
mydb = client["Personal-Cluster-db"] #connects to db but if not found will create it 
table1 = mydb["hiders"] #connects to table but if not found will create it 
# table2 = mydb["Quiz"]


print(table1)

data = {
    "username":"Maya",
    "found":"Not yet",
    "Image":"Image link"
}
table1.insert_one(data) #inserts into db
client.close()