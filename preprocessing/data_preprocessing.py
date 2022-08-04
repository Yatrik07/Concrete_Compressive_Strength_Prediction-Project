import pandas as pd
from App_Logging.Logging import get_logs
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
import joblib
class preprocess:
    '''
    class name : preprocess

    description : This class and methods are to preprocess the data.

    Written By : Yatrik Shah
    '''

    def __init__(self):

        self.logger = get_logs( open('Logs//preprocessing.txt' , "a" ))
        self.logger.write_logs("Entered Preprocessing Directory.")

    def scaling(self , data):
        '''
        method name : scaling

        description : This method is defined to scale the data to fit into Machine Learning Model.

        parameters : data
            data : This input parameter is the required data to scale

        returns : scaled data

        Written by : Yatrik Shah
        '''

        self.logger.write_logs("Entered scaling method.")
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        self.logger.write_logs("Data scaled successfully.")
        joblib.dump(scaler , "models//Preprocessing Models//scaler.pickle")
        return scaled_data

    def separate_X_Y(self , full_data):
        '''
        method name : separate_X_Y

        description : This method basically separates the input parameters X and label column y

        parameters : full_data

        return : X , y

        written by : Yatrik Shah
        '''

        self.logger.write_logs("Entered separate_X_Y method.")
        X = full_data.drop("concrete_compressive_strength" , axis=1)
        y = full_data[['concrete_compressive_strength']]

        self.logger.write_logs("Separated X and y from the data successfully.")
        return X , y


    def Data_Imputation(self , data):
        '''
        method name : Data_Imputation

        description : -> Given the data, if there are some missing values or Null values then impute them.

                      -> If there are significant number of missing or Null values in a single TrainingBatchFile
                            then move it to BadDataFolder.

        parameters : data

        returns : Imputed Data or Raise Exception
        '''
        if data.isna().sum().sum() < 0.35 * (data.shape[0]*data.shape[1]):
            pass



