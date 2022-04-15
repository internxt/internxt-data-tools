from pymongo import MongoClient
import pandas as pd

class Mongo:
  def __init__(self, uri, db):
    self.client = MongoClient(uri)
    self.db = self.client[db]

  def get_users(self):
    users = self.db.users
    cursor = users.find()
    df = pd.DataFrame(list(cursor))
    cols = list(df.columns)

    for c in ['_id', 'maxSpaceBytes', 'uuid']:
      cols.remove(c)

    df = df.rename(columns={"_id": "email", "maxSpaceBytes": "storage", "uuid": "userId"})
    df = df.astype({"email": str, "userId": str})
    df["storage"] = pd.to_numeric(df["storage"], errors='coerce')

    return df


