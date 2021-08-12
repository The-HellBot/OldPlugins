from pymongo import MongoClient
from pymongo.errors import ConfigurationError

import os
import logging
try:



         
    MONGO_DB_URL = os.environ.get("MONGO_DB_URL", None)

    client =  MongoClient(MONGO_DB_URL)


except ConfigurationError:
    logging.info("Mongo DB URL Incorrect!, check whats wrong with it ")
    

except Exception as e:
   logging.info("Failed Connection with mongo")

sed = client['Hell']
db = sed['datas']
