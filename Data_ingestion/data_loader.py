import pandas as pd
from App_Logging.Logging import get_logs


class input_data_loader:
    '''
    class name : input_data_loader

    description : This class loads different input data file(s).

    Written by : Yatrik Shah
    '''

    def __init__(self):
        self.logger = get_logs( open("Logs//Training_dataIngestion_validation_logs.txt" , "a") )
        self.logger.write_logs("Entered data_loader directory")


    def get_raw_data(self):
        self.logger.write_logs("Entered get_raw_data method")
        filepath = "training_data//"
        filename = "concrete_data.csv"
        df = pd.read_csv(filepath+filename)
        self.logger.write_logs("Returning raw_data.")
        return df


    ''' fuction in model_train.py
    def Get_TriningBatchData(self):
        Valid_dataFiles = self.Training_Validations()

        with open("schema_training.json", "r") as read_it:
            self.schemaTraining_json = json.load(read_it)

        columns = list(self.schemaTraining_json['ColName'].keys())

        finalTraining_df = pd.DataFrame(columns=columns)

        for datafile in Valid_dataFiles:
            df = pd.read_csv("Training_BatchFiles//" + datafile)
            finalTraining_df = pd.concat([finalTraining_df, df], axis=0)

        database = DBOperations()
        database.Dataframetodatabase(finalTraining_df)
    '''
