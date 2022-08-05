import sqlite3
from App_Logging.Logging import get_logs
import pandas as pd


class DBOperations:
    def __init__(self):
        self.logger = get_logs( open("Logs//DatabaseOperations.txt" , "a+"))

    def create_Database_Table(self):
        """
        Method Name : create_Database_Table

        Description : This method is written to create/connect database TrainingData.db and
                      Create / delete-Create table in database 'Train' used to save training data.

        Parameters : None

        Returns : None

        Written By : Yatrik Shah
        """
        self.logger.write_logs("Entered function create_Database_Table.")
        conn = sqlite3.connect('TrainingDatabase//TrainingData.db')
        self.logger.write_logs("Created / Connected TrainingData Database successfully!")
        cursor_obj = conn.cursor()
        cursor_obj.execute('''CREATE TABLE if not exists Train(cement Float, blast_furnace_slag Float, fly_ash Float, water Float, superplasticizer Float,
                                   coarse_aggregate Float, fine_aggregate Float, age Integer)''');
        self.logger.write_logs("Train Table created successfully!")
        conn.close()

    def enter_recordTo_Table(self , cement, blast_furnace_slag, fly_ash, water, superplasticizer, coarse_aggregate, fine_aggregate, age):
        """
        Method Name : enter_recordTo_Table

        Description : This method is written to enter a single/multiple record to the Train table

        Parameters : column Values for the table

        Returns : None

        Written By : Yatrik Shah
        """
        self.logger.write_logs("Entered function enter_recordTo_Table.")
        conn = sqlite3.connect('TrainingDatabase/TrainingData.db')
        cursor_obj = conn.cursor()
        cursor_obj.execute(
            "insert into TESTED(cement, blast_furnace_slag, fly_ash, water, superplasticizer, coarse_aggregate, fine_aggregate, age) values(?,?,?,?,?,?,? )",
            [cement, blast_furnace_slag, fly_ash, water, superplasticizer, coarse_aggregate, fine_aggregate, age])
        conn.commit()
        conn.close()

    def showTable(self):
        """
        Method Name : showTable

        Description : This method is written to show the table Train.

        Parameters : None

        Returns : None

        Written By : Yatrik Shah
        """
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
        """
        Method Name : dropTabel

        Description : This method is written to drop the table Train if already exists.

        Parameters : None

        Returns : None

        Written By : Yatrik Shah
        """
        self.logger.write_logs("Entered function dropTabel.")
        conn = sqlite3.connect('TrainingDatabase/TrainingData.db')
        cursor_obj = conn.cursor()
        cursor_obj.execute('''drop table if exists Train''')
        conn.commit()
        conn.close()
        self.logger.write_logs("Table Train dropped successfully.")

    def show_all_tables(self):
        """
        Method Name : show_all_tables

        Description : This method is written to show all the tables exists in the database TrainingData.db .

        Parameters : None

        Returns : None

        Written By : Yatrik Shah
        """
        conn = sqlite3.connect('TrainingDatabase/TrainingData.db')
        cursor_obj = conn.cursor()
        cursor_obj.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor_obj.fetchall())

    def Dataframetodatabase(self, data):
        """
        Method Name : Dataframetodatabase

        Description : This method is written to save the entire dataframe into the Train schema into TrainingData.db .

        Parameters : data : The data to convert into the database schema

        Returns : None

        Written By : Yatrik Shah
        """
        self.logger.write_logs("Entered function Dataframetodatabase.")
        conn = sqlite3.connect(os.path.join('TrainingDatabase' , 'TrainingData.db') )
        try:
            data.to_sql(name='Train', con=conn , index=False)
        except:
            conn.execute("DROP TABLE Train")
            data.to_sql(name='Train', con=conn, index=False)


    def getDatafromDatabase(self):
        """
        Method Name : getDatafromDatabase

        Description : This method is written to get the Training data in form of pandas dataframe from Train schema TrainingData.

        Parameters : None

        Returns : Training data from schema 'Train'

        Written By : Yatrik Shah
        """
        connection = sqlite3.connect('TrainingDatabase//TrainingData.db')
        data = pd.read_sql_query("SELECT * FROM Train", connection)
        return data


