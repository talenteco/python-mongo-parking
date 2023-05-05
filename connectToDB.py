
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

load_dotenv()

def connectToMongo():
    uri = os.environ.get('MONGO_URI')
    client = MongoClient(uri)

    try:
        client.admin.command('ping')
        print("Pinged deployment. You successfully connected to MongoDB!")
        return(client)

    except Exception as e:
        print(e)
        return(False)
