from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
import pandas as pd
from App_Logging.Logging import get_logs
import joblib

class Create_Clusters:
    '''
    class name : Create_Clusters

    Description : This class is written to help for creating different clusters form the data.

    Paramneters : None

    Written By : Yatrik Shah
    '''

    def __init__(self):
        self.logger = get_logs( open( "Logs//clustering.txt" , "a"))
        self.logger.write_logs("Entered Clustering class.")


    def silhoutte_score(self, data):
        '''
        method name : silhoutte_score

        description : -> Given the data, this method fits K-Means model with different values of K and returns
                      the number of clusters with the maximum number of the silhoutte-score and summary of
                      silhoutte-score with different values of k also.

                      -> Basically used for clustering of the data

        parameters : data

        returns : K with maximum silhoutte score , summary
        '''

        self.logger.write_logs("Entered silhoutte_score method.")

        K_values = range(2, 9)

        silhoutte_list = []
        for k in K_values:
            model = KMeans(n_clusters=k)
            model.fit(data)
            labels = model.predict(data)
            score = silhouette_score(data, labels)
            silhoutte_list.append(score)

        final_k_value = pd.Series(data=silhoutte_list, index=K_values).idxmax()
        self.logger.write_logs(
            f"Successfully got {final_k_value} as a final k value for clustering with {silhoutte_list[final_k_value - 2]} silhoutte score.")
        print(final_k_value, list(zip(silhoutte_list, K_values)))
        return final_k_value, list(zip(silhoutte_list, K_values))

    def Create_Clusters_From_Data(self, Data , NumberOfClusters):
        '''
        method name : Create_Clusters_From_Data

        description : -> Given the data, this method fits K-Means model on the data and then predicts cluster
                          of each single data point and save them as a column in the given data
                          and returns that updated one data.

        parameters : data

        returns : given data with one added column as culster , where respective cluster number is stored
         in that cluster column.
        '''

        self.logger.write_logs("Entered Create_Clusters_From_Data method.")
        df = Data
        model = KMeans(random_state=100 , n_clusters=NumberOfClusters)
        model.fit(df)
        self.logger.write_logs("Fitted clustering model on the data.")
        labels = model.predict(df)
        df['cluster'] = labels
        joblib.dump(model , "models//Preprocessing Models//clustering_model.pickle")

        self.logger.write_logs("Returning Updated data from 'Create_Clusters_From_Data' method with one added column 'cluster'.")
        return df


