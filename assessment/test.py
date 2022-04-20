import csv
import json
import sqlalchemy

# connect to the database
engine = sqlalchemy.create_engine("mysql://datatest:alligator@database/datatestdb")
connection = engine.connect()

metadata = sqlalchemy.schema.MetaData(engine)

# make an ORM object to refer to the table
Example = sqlalchemy.schema.Table('examples', metadata, autoload=True, autoload_with=engine)


# read the CSV data file into the table
with open('/data/test.csv') as csv_file:
  reader = csv.reader(csv_file)
  next(reader)
  for row in reader: 
    connection.execute(Example.insert().values(name = row[0]))

# output the table to a JSON file
with open('/data/test.json', 'w') as json_file:
  rows = connection.execute(sqlalchemy.sql.select([Example])).fetchall()
  rows = [{'id': row[0], 'name': row[1]} for row in rows]
  json.dump(rows, json_file, separators=(',', ':'))

print("Test Successful")