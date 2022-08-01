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
