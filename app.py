import numpy as np
import flask
import flask_cors
import joblib
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from App_Logging.Logging import get_logs
import warnings
from DatabaseInsertion.DatabaseOperartions import DBOperations
warnings.filterwarnings("ignore")


app = flask.Flask(__name__)
logger = get_logs( open("Logs//homepageLogs.txt" , "a"))


@app.route('/', methods=['GET', "POST"])
@cross_origin()
def home_page():
    logger.write_logs("Someone Entered Homepage, Rendering Homepage!")
    return render_template("form.html")


@app.route('/prediction', methods=['GET', 'POST'])
@cross_origin()
def pred_page():
    try:
        if request.method == 'POST':
            logger.write_logs("Left Home Page.")
            cement = float(request.form["cement"])
            blast_furnace_slag = float(request.form["blast_furnace_slag"])
            fly_ash = float(request.form["fly_ash"])
            water = float(request.form["water"])
            superplasticizer = float(request.form["superplasticizer"])
            coarse_aggregate = float(request.form["coarse_aggregate"])
            fine_aggregate = float(request.form["fine_aggregate"])
            age = float(request.form["age"])

            logger.write_logs("Successfully taken input values from user")

            input = np.array([cement, blast_furnace_slag, fly_ash, water, superplasticizer,
                               coarse_aggregate, fine_aggregate, age]).reshape(1, 8)

            output = get_Prediction(input)

            return render_template('prediction.html' , result = output)

    except ValueError:
        return render_template('Error.html' , result = f"Invalid Input")

    except Exception as e:
        return render_template('Error.html' , result = f"Some Error Occured {e}")




@app.route('/train', methods=['GET', 'POST'])
@cross_origin()
def train():
    logger.write_logs("Entered /train path , ReTraining model.")
    from  model_train import Trainer
    trainer = Trainer()
    trainer.Get_TriningBatchData()
    database = DBOperations()
    df = database.getDatafromDatabase()
    trainer.Preprocessing_clustering(df)
    trainer.training_clusterd_data()
    return render_template('Message.html', result="Successfully Retrained Model.")


def get_objects():
    """
    Method Name : get_objects
    Description : This method is written to get the scaler and the clustering objects those are saved in serialized  format.
    Parameters : None
    Returns : scalerobject , clusteringObject
    Written By : Yatrik Shah
    """
    logger.write_logs("Entered get_objects function.")
    scaler = joblib.load("models//Preprocessing Models//scaler.pickle")
    clustering = joblib.load("models//Preprocessing Models//clustering_model.pickle")
    logger.write_logs("Returning scaling and clustering objects from get_objects function.")
    return scaler ,clustering

def get_Prediction(input):
    """
    Method Name : get_Prediction
    Description : This method is written to get the predicted output given the input.
                  It applies the scaling operation , clustering operation and then calls the model according
                  to the respective cluster.
    Parameters : input
    Returns : PredictedOutput
    Written By : Yatrik Shah
    """
    logger.write_logs("Entered get_Prediction function.")
    scaler, clustering = get_objects()
    input = scaler.transform(input)
    cluster_number = clustering.predict(input)
    model = joblib.load(f"models//cluster-{str(int(cluster_number[0]))}//final_model.pickle")
    output = model.predict(input)
    output = str( round(  float(output[0]) ,2 ))
    logger.write_logs("Returning output from get_Predictions function..")
    return output

if _name_ == "__main__":
    app.run()
