import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error , r2_score
from App_Logging.Logging import get_logs

from sklearn.model_selection import train_test_split


class FindBestModel:
    '''
    class name : FindBestModel

    parameters : X ,y , cluster_number
        x : Features of Data [ excluding target column ] [ Independent columns ]
        y : Target column
        cluster_number : This is just a name respective which the models are saved in serialized formats

          work : This class is created to find th best model out of all
            Used Algorithms : 1. RandomForest
                              2. XGBoost
    '''

    def __init__(self ,X ,y, cluster_number):
        self.X = X
        self.y = y
        self.cluster_number = cluster_number
        self.logger = get_logs( open("Logs//Model_Selection.txt" , 'a'))
        self.logger.write_logs(f"For cluster-{self.cluster_number}, Entered FindBestModel class in Cross_Validation_ModelSelection//best_model_finder.py")

    def RandomForest(self, grid):
        '''
        method name : RandomForest

        parameters : grid
            grid : multiple combinations of hyperparameters of Randomforest model to test on the given data

        work :
        Performs Randomforset Regression on given dataset after splitting it into train and test set.
        Checks for best parameters of the model according to the dataset

        return :
         1. The best parameters of the model i.e. XG_gridSearch.best_params
         2. Best estimators of the model i.e. XG_gridSearch.best_estimator
         3. Root Mean Squaed error of the model with best parameters on the test dataset
         4. Coefficient of Determination (R squared ) of the model on given dataset
        '''

        # print("Random Forest for ",self.cluster_number)
        self.logger.write_logs(
            f"Random Forest for {self.cluster_number}")
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, random_state=1, test_size=0.3)
        RF_model = RandomForestRegressor()
        rf_gridSearch = GridSearchCV(RF_model, param_grid=grid , verbose=3, cv = 5 , n_jobs=-1 , scoring="neg_mean_squared_error")
        rf_gridSearch.fit(X_train, y_train)
        rf_prediction = rf_gridSearch.predict(X_test)
        RF_RMSE = np.sqrt(mean_squared_error(y_test, rf_prediction))
        RF_r2=  r2_score(y_test , rf_prediction)

        rf_train_prediction = rf_gridSearch.predict(X_train)
        RF_train_RMSE = np.sqrt(mean_squared_error(y_train, rf_train_prediction))
        RF_train_r2 = r2_score(y_train, rf_train_prediction)

        # try:
        #     os.rmdir("models")
        # except:
        #     pass
        # try:
        #     os.mkdir(f"models" )
        #     os.mkdir(f"models//cluster-{self.cluster_number}")
        # except:
        #     raise Exception
        #
        #
        # joblib.dump(rf_gridSearch, f"models//cluster-{self.cluster_number}//RandomForestModel_"+self.cluster_number+"_.pickle")
        self.logger.write_logs(
            f"Got best parameers for cluster-{self.cluster_number}")

        return rf_gridSearch.best_params_, rf_gridSearch.best_estimator_, RF_RMSE , RF_r2, RF_train_RMSE, RF_train_r2 , rf_gridSearch

    def XGBoost(self, grid):
        '''
        method name : XGBoost

        parameters : grid
            grid : multiple combinations of hyperparameters of XGBoost model to test on the given data

        work:
        Performs XGBoost Regression on given dataset after splitting it into train and test set.
        Checks for best parameters of the model according to the dataset

        return :
         1. The best parameters of the model i.e. XG_gridSearch.best_params
         2. Best estimators of the model i.e. XG_gridSearch.best_estimator
         3. Root Mean Squaed error of the model with best parameters on the test dataset
         4. Coefficient of Determination (R squared ) of the model on given dataset
        '''
        # print("XGBOOST for ",self.cluster_number)
        self.logger.write_logs(
            f"XGBoost for {self.cluster_number}")
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, random_state=1, test_size=0.3)
        XG_model = XGBRegressor()
        XG_gridSearch = GridSearchCV(XG_model, param_grid=grid , verbose=3 , cv = 5, scoring = 'neg_mean_squared_error', n_jobs = -1)
        XG_gridSearch.fit(X_train, y_train)
        XG_prediction = XG_gridSearch.predict(X_test)
        XG_RMSE = np.sqrt(mean_squared_error(y_test, XG_prediction))
        XG_r2 = r2_score(y_test , XG_prediction)
        XG_train_prediction = XG_gridSearch.predict(X_train)
        XG_train_RMSE = np.sqrt(mean_squared_error(y_train, XG_train_prediction))
        XG_train_r2 = r2_score(y_train, XG_train_prediction)
        #
        # try:
        #     os.rmdir("models")
        # except:
        #     pass
        # try:
        #     os.mkdir(f"models" )
        #     os.mkdir(f"models//cluster-{self.cluster_number}")
        # except Exception:
        #     print(Exception)
        #
        # joblib.dump(XG_gridSearch,f"models//cluster-{self.cluster_number}//XGBoostModel_"+self.cluster_number+"_.pickle")
        return XG_gridSearch.best_params_, XG_gridSearch.best_estimator_, XG_RMSE , XG_r2, XG_train_RMSE, XG_train_r2 , XG_gridSearch

    def best_model(self, xgboost_grid , rf_grid):
        '''
        method name : best_model

        parameters : xgboost_grid , rf_grid
            xgboost_grid :  multiple combinations of hyperparameters of XGBoost model to test on the given data
            regarding XGBoost Model

            rf_grid :   multiple combinations of hyperparameters of XGBoost model to test on the given data
            regarding RandomForest Model

        work :
        This functions finds the best model out of all models preformed [ XGBOOST ang RANODMFOREST ]
        and returns best parameters and Root Mean Squared Error of the best Model out of all
        This method  uses the created userdefined functions "RandomForest" and "XGBoost"

        return :
        returns the output of the "XGBoost" and "RandomForest" function respectively in form of list
        '''
        RF = self.RandomForest(rf_grid)
        XG = self.XGBoost(xgboost_grid)
        self.logger.write_logs("\n\nCluster :" + str(self.cluster_number))
        self.logger.write_logs("Random Forest:"+ str(RF))
        self.logger.write_logs("\nRandom Forest Error" + str(RF[2]))
        self.logger.write_logs("\n RF r2 score : "+str(RF[3]))
        self.logger.write_logs("\n\nXGBOOST:"+ str(XG))
        self.logger.write_logs("\nXGBOOST Error"+ str(XG[2]))
        self.logger.write_logs("\n XGB r2 score : "+str(XG[3]))

        try:
            os.mkdir(f"models" )
        except:
            pass
        try:
            os.mkdir(f"models//cluster-{self.cluster_number}")
        except Exception as e:
            print(e)


        if RF[3] > XG[3]:
            joblib.dump(RF[6] , f"models//cluster-{self.cluster_number}//final_model.pickle")
        else :
            joblib.dump(XG[6], f"models//cluster-{self.cluster_number}//final_model.pickle")

        return [XG , RF]


