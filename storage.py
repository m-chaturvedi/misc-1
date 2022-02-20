import sqlite3
from config import Config

class SqlStorage():
  def __init__(self, table_name=Config.table_name, db_name=Config.database_name):
    self.table_name = table_name
    self.database_name = db_name
    self.table_type = Config.sensor_table_types
    self.connection = sqlite3.connect(db_name)
    self.cursor = self.connection.cursor()
    self.create_table()

  def create_table(self):
    key_val = []
    for k in self.table_type:
      val = self.table_type[k]
      key_val.append(f"{k} {val}")

    key_val_str = ", ".join(key_val)
    self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({key_val_str})")
    self.connection.commit()

  def append_to_table(self, **kwargs):
    query_list = []
    for key in Config.sensor_table_types:
      query_list.append(kwargs[key])

    questions = ", ".join(["?"]*len(query_list))
    self.cursor.execute(f"INSERT INTO {self.table_name} VALUES ({questions})", tuple(query_list))
    self.connection.commit()
