
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
logger = get_logs("homepageLogs.txt")


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

    except:
        return render_template('Error.html' , result = "Invalid Input")




@app.route('/train', methods=['GET', 'POST'])
@cross_origin()
def train():
    from  model_train import Trainer
    trainer = Trainer()
    trainer.Get_TriningBatchData()
    database = DBOperations()
    df = database.getDatafromDatabase()
    trainer.Preprocessing_clustering(df)
    trainer.training_clusterd_data()

def get_objects():
    scaler = joblib.load("models//Preprocessing Models//scaler.pickle")
    clustering = joblib.load("models//Preprocessing Models//clustering_model.pickle")
    return scaler ,clustering

def get_Prediction(input):
    scaler, clustering = get_objects()
    input = scaler.transform(input)
    cluster_number = clustering.predict(input)
    model = joblib.load(f"models//cluster-{str(cluster_number)}//final_model.pickle")
    output = model.predict(input)
    return output

if __name__ == "__main__":
    app.run()






