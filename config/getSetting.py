from pymongo import MongoClient
import os
import sys
import logging
def getSetting(setting:str|None):
    if setting == None:
        return "None"
    from pymongo import MongoClient
    CONNECTION_STRING = os.getenv("MONGO_connection_string")
    client: MongoClient = MongoClient(CONNECTION_STRING)
    database = os.getenv("MONGO_maindb")
    if database == None:
        logging.info("BAD ENV MONGO_maindb")
        sys.exit()
    
    db = client[database]
    collection = os.getenv("MONGO_settings_collection")
    if collection == None:
        logging.info("BAD ENV MONGO_settings_collection")
        sys.exit()
    
    settings = db[collection]
    result = settings.find_one(setting)
    if not result:
        return "None"
    return result["value"]