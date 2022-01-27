import mysql.connector
from openpyxl import load_workbook
from openpyxl.descriptors.serialisable import KEYWORDS
from ConfigManager import ConfigManager


db_config = ConfigManager.get_config("db")

db = mysql.connector.connect(
  host=db_config["host"],
  user=db_config["user"],
  password=db_config["password"],
  database=db_config["db"]
)

cursor = db.cursor()

SQL = "INSERT INTO full_region_info (id, simple_id, depth1, depth2, depth3) VALUES (%s, %s, %s, %s, %s)"

workbook = load_workbook("./hcode_list.xlsx", data_only=True)
sheet = workbook['list']
rows = sheet.rows

insert_values = []
for simple_id, id, dep1, dep2, dep3 in rows:
  insert_values.append([id.value, simple_id.value, dep1.value, dep2.value, dep3.value])

cursor.executemany(SQL, insert_values)
db.commit()
print(cursor.rowcount, "was inserted.")