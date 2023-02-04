import numpy as np
import pickle

from datetime import datetime

import boto3
from decimal import Decimal



def lambda_handler(event, context):
    '''
    The event is a JSON pass with the informations that we pass to our model to make predictions.
    In our case, our event is going to be like:
        event = {
            "X" = [list with points to make the prediction], 
            "user": {
                "username": "user name", 
                "age": user age (int)
            }
        }
    since we want to use DynamoDB (a non relational database) to put our requests.

    Return:
        prediction value (float) according to X.
    '''

    user_informations = event["user"]
    X = event["X"]

    model_file = "linear_model.bin"
    with open(model_file, "rb") as f_in: # Reading the binary file
        model = pickle.load(f_in)

    
    X = np.array(X).reshape(-1, 1)

    predict_at = datetime.now()
    y_pred = model.predict(X)

    dynamoDB_table = dynamoDB_integration() # Primary Key: "username"
    # Informations to put in the DynamoDB Table
    values = [Decimal(str(round(y_predict, 3))) for y_predict in y_pred]
    user_infos = {
        "username": user_informations["username"],
        "age": user_informations["age"], 
        "predictions": {
            "predict_at": str(predict_at), 
            "values": values
        }
    }
    # Saving the information in the database
    dynamoDB_table.put_item(Item=user_infos)

    return {
        "predictions": {
            "predict_at": str(predict_at), 
            "values": values
        }
    }


def dynamoDB_integration():
    '''
    This function is used to access the DynamoDB database. 
    Note that we do not pass any AWS key because we are going to use this function inside a Dcoker
    image inside AWS enviroment.
    '''
    db =  boto3.resource(service_name = "dynamodb", region_name="us-east-1")
    table = "UserPrediction" # The name that we are going to use for our DynamoDB table 

    return db.Table(table)
