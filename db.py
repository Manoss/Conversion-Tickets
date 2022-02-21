import pymongo

clientdb = pymongo.MongoClient("mongodb://localhost:27017/")

def connectdb():
    #clientdb = pymongo.MongoClient("mongodb://localhost:27017/")
    db = clientdb["ticket"]
    collection = db["tickets"]
    return collection

def insertdb(dict, collection):
    collection.insert_one(dict)

def closedb():
    clientdb.close()



