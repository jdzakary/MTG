import sqlalchemy as db
import pandas as pd

engine = db.create_engine('sqlite:///../Database_Files/main_database.db')
data = pd.read_sql('select * from collection_1 where collection_id = 5', engine)
print(data)
