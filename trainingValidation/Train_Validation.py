from os import listdir , rmdir
from os.path import isfile, join
import pandas as pd
import re
from App_Logging.Logging import get_logs
import json

# mypath = "..//training_data"
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# print(onlyfiles)


logger = get_logs( open("Logs//Training_dataIngestion_validation_logs.txt" , "a"))
class Validations:
    def __init__(self):
        logger.write_logs("Entered Validation Class in Training Validation.")

        with open("schema_training.json", "r") as read_it:
            self.schemaTraining_json = json.load(read_it)

        logger.write_logs("Loaded schema_training.json file for reference.")


    def RegexCreationForFileName(self):
        '''
        Method Name : RegexCreationForFileName

        Description : Creates Regular Expression for the training Data Batch files.

        Parameters : None

        Written By : Yatrik Shah
        '''
        logger.write_logs("Entered RegexCreationForFileName method in Training_Validation.")
        regex = "['cement_strength']+['\_'']+[\d_]+[\d]+\.csv"

        return regex

    def CheckColumn_Name_Numbers(self , file_name):
        '''
        Method Name : CheckColumn_Name_Numbers

        Description : This method is written to check if the given training csv batchFile columns names and
                       number of columns are same as expected or not.
                        If not then moved to Bad_Data_Folder.
                        Otherwise considered for further validation and Model Training.Validations

        Parameters : file_name

        Returns :
         True : If all the columns names and total number of column are same as expected.
         False : O/W

        Written By : Yatrik Shah
        '''


        # print("\njson keys:\n",self.schemaTraining_json.keys())
        # print("\nColName\n",self.schemaTraining_json['ColName'])
        # print("\nColName1\n", list(self.schemaTraining_json['ColName'].keys()))
        columns = list(self.schemaTraining_json['ColName'].keys())
        No_of_cols = len(columns)

        logger.write_logs("Entered in the method CheckColumn_Name_Numbers.")
        df = pd.read_csv("Training_BatchFiles//"+file_name)

        Flag = True

        if (len(df.columns)==No_of_cols) and ( sum((df.columns == columns))  == 9) :
            pass

        else:
            print("\n\n",file_name)
            print(len(df.columns)==No_of_cols)
            print(sum((df.columns == columns)) == 9)
            print(list(df.columns))
            print(columns)
            print("\n\n")
            Flag = False


        if Flag:
            logger.write_logs("All columns Name and Number are same as expected.")
        else:
            logger.write_logs("All columns Name and Number are not same as expected.")

        return Flag



    def CheckColumnDatatype(self , file_name):
        '''
        Method Name : CheckColumnDatatype

        Description : This method is written to check the respective datatypes of the respective columns if they
                       are same as expected or not. If not then moved to Bad_Data_Folder. Otherwise considered
                       for further validation and Model Training.Validations

        Parameters : file_name

        Returns :
         True : If all the columns datatype are as expected.
         False : O/W

        Written By : Yatrik Shah
        '''
        correct_datatypes  = list(self.schemaTraining_json['ColName'].values())
        logger.write_logs("Entered in the method CheckColumnDatatype.")
        try:
            df = pd.read_csv("Training_BatchFiles//"+file_name)
        except:
            logger.write_logs("Passed Invalid file_name... Exiting the function")
            raise Exception("Invalid FileName")
        dtypes = []
        for col in df.columns:
            dtypes.append(df[col].dtype)

        Flag = True
        for dtype,correct_datatype in zip(dtypes ,correct_datatypes):
            if correct_datatype=="FLOAT" and [str(dtype).startswith("float") or str(dtype).startswith("int")]:
                pass
            elif correct_datatype=="INTEGER" and [str(dtype).startswith("float") or str(dtype).startswith("int")]:
                pass
            else:
                # print(str(dtype))
                Flag = False



        # logger.write_logs("Successfully checked Column Datatypes.")

        if Flag:
            logger.write_logs("Successfully checked Column Datatypes.")
            logger.write_logs("Column Datatypes are same as expected.")

        else:
            logger.write_logs("Successfully checked Column Datatypes.")
            logger.write_logs("Column Datatypes are not same as expected.")

        return Flag


    def delete_Good_Data_Bad_Data_Folder(self):
        '''
        Method_name : delete_Good_Data_Bad_Data_Folder

        Description : This method deletes "Good_Data_Folder" and "Bad_Data_Folder" is already exists.self

        Parameters : None

        return : None

        Written By : Yatrik Shah
        '''
        logger.write_logs("Entered delete_Good_Data_Bad_Data_Folder method.")
        try:
            rmdir("GoodDataFolder")
            logger.write_logs("Successfully removed GoodDataFolder.")
        except:
            logger.write_logs("There is not GoodDataFolder available initially.")
            pass
        try:
            rmdir("BadDataFolder")
            logger.write_logs("Successfully removed BadDataFolder.")
        except:
            logger.write_logs("There is not BadDataFolder available initially.")
            pass



    def getTrainingBatchFiles(self):
        mypath = "Training_BatchFiles"
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        # print(onlyfiles)
        return onlyfiles


    def matchRegularExpression(self,  file_name):
        regex = self.RegexCreationForFileName()
        Flag = True if re.match(regex , file_name) else False

        return Flag



