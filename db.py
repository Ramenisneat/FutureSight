from pymongo import MongoClient

def get_db():

   CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net/devices"
   client = MongoClient(CONNECTION_STRING)
   return client['devices']
  
if __name__ == "__main__":   
   dbname = get_database()