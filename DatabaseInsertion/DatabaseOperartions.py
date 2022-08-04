import sqlite3
from App_Logging.Logging import get_logs
import pandas as pd


class DBOperations:
    def __init__(self):
        self.logger = get_logs( open("DatabaseOperations.txt" , "a+"))

    def create_Database_Table(self):
        self.logger.write_logs("Entered function create_Database_Table.")
        conn = sqlite3.connect('TrainingDatabase//TrainingData.db')
        self.logger.write_logs("Created / Connected TrainingData Database successfully!")
        cursor_obj = conn.cursor()
        cursor_obj.execute('''CREATE TABLE if not exists Train(cement Float, blast_furnace_slag Float, fly_ash Float, water Float, superplasticizer Float,
                                   coarse_aggregate Float, fine_aggregate Float, age Integer)''');
        self.logger.write_logs("Train Table created successfully!")
        conn.close()

    def enter_recordTo_Table(self , cement, blast_furnace_slag, fly_ash, water, superplasticizer, coarse_aggregate, fine_aggregate, age):
        self.logger.write_logs("Entered function enter_recordTo_Table.")
        conn = sqlite3.connect('TrainingDatabase/TrainingData.db')
        cursor_obj = conn.cursor()
        cursor_obj.execute(
            "insert into TESTED(cement, blast_furnace_slag, fly_ash, water, superplasticizer, coarse_aggregate, fine_aggregate, age) values(?,?,?,?,?,?,? )",
            [cement, blast_furnace_slag, fly_ash, water, superplasticizer, coarse_aggregate, fine_aggregate, age])
        conn.commit()
        conn.close()

    def showTable(self):
        self.logger.write_logs("Entered function showTable.")
        conn = sqlite3.connect('TrainingDatabase/TrainingData.db')
        cursor_obj = conn.cursor()
        output = cursor_obj.execute("select * from Train")

        data = cursor_obj.execute('''SELECT * FROM Train''')
        for column in data.description:
            print(column[0] , end="\t")
        print("")
        for row in output:
            print(row)
        conn.close()

    def dropTabel(self):
        self.logger.write_logs("Entered function dropTabel.")
        conn = sqlite3.connect('TrainingDatabase/TrainingData.db')
        cursor_obj = conn.cursor()
        cursor_obj.execute('''drop table if exists Train''')
        conn.commit()
        conn.close()
        self.logger.write_logs("Table Train dropped successfully.")

    def show_all_tables(self):
        conn = sqlite3.connect('TrainingDatabase/TrainingData.db')
        cursor_obj = conn.cursor()
        cursor_obj.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor_obj.fetchall())

    def Dataframetodatabase(self, data):

        self.logger.write_logs("Entered function Dataframetodatabase.")
        conn = sqlite3.connect('TrainingDatabase/TrainingData.db')
        try:
            data.to_sql(name='Train', con=conn , index=False)
        except:
            conn.execute("DROP TABLE Train")
            data.to_sql(name='Train', con=conn, index=False)


    def getDatafromDatabase(self):
        connection = sqlite3.connect('TrainingDatabase//TrainingData.db')
        data = pd.read_sql_query("SELECT * FROM Train", connection)
        return data


