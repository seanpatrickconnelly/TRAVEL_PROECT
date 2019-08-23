import os

import pandas as pd
import numpy as np
import json as json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', '') or "sqlite:///db/airline_data.sqlite"
db = SQLAlchemy(app)

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Flights = Base.classes.Flights

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/reasons")
def reasons():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Flights).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the delay reasons for dropdown
    return jsonify(["All Delays", "Airline", "Late-Arriving Aircraft", "NAS", "Security", "Weather"])


@app.route("/samples/<sample>")
def samples(sample):
    """Return `AirportCode`, `TotDelayArrFlight`,and `sample_values`."""
    stmt = db.session.query(Flights).statement
  
    df = pd.read_sql_query(stmt, db.session.bind)
   
    #groupby then sum or avg the time

    # print(df.columns)
    #print(df.head())
    # Filter the data based on the sample number and
    # only keep rows with values above 1
    
    if sample == 'TotDelayArrFlight':
        sample_time = 'TotMinArrDelay'
    elif sample == "airlineDelay":
        sample_time = "AirlineDelayTime"
    elif sample == "lateAircraftDelay":
        sample_time = "LateAircraftDelayTime"
    elif sample == "nasDelay":
        sample_time = "nasDelayTime"
    elif sample == "securityDelay":
        sample_time = "SecurityDelayTime"
    elif sample == "weatherDelay":
        sample_time = "WeatherDelayTime"

    sample_data = df.loc[df[sample] > 1, ["AirportCode", sample, sample_time]]

    # # # Sort by sample
    # sample_data.sort_values(by=sample, ascending=False, inplace=True)

    df_airport_sum = sample_data.groupby('AirportCode').sum()
    df_airport_sum_drop = df_airport_sum.drop(columns = sample_time)
    df_airport_mean = sample_data.groupby('AirportCode').mean()
    df_airport_mean_drop = df_airport_mean.drop(columns = sample)

    df_final = df_airport_sum_drop.merge(df_airport_mean_drop,left_on='AirportCode',right_on='AirportCode')
    df_final = df_final.reset_index()
    # df_final.to_csv('test.csv')

    # Format the data to send as json
    data = {
        "AirportCode": df_final.AirportCode.values.tolist(),
        "Count" : df_final[sample].values.tolist(),
        "Time" : df_final[sample_time].values.tolist(),
    }
    # return jsonify(json.loads(sample_data.to_json(orient='records')))
    return jsonify(data)

@app.route("/samples1/<sample1>")
def samples1(sample1):

    stmt = db.session.query(Flights).statement

    df = pd.read_sql_query(stmt, db.session.bind)

    if sample1 == 'TotDelayArrFlight':
        sample1_time = 'TotMinArrDelay'
    elif sample1 == "airlineDelay":
        sample1_time = "AirlineDelayTime"
    elif sample1 == "lateAircraftDelay":
        sample1_time = "LateAircraftDelayTime"
    elif sample1 == "nasDelay":
        sample1_time = "nasDelayTime"
    elif sample1 == "securityDelay":
        sample1_time = "SecurityDelayTime"
    elif sample1 == "weatherDelay":
        sample1_time = "WeatherDelayTime"

    sample1_data = df.loc[df[sample1] > 1, ["AirportCode", sample1_time]]

    df_airport_mean_1 = sample1_data.groupby('AirportCode').mean()
    # df_airport_mean_1.to_csv('test.csv')
    df_airport_mean_1 = df_airport_mean_1.reset_index()
    df_airport_mean_1.sort_values(by=sample1_time, ascending=True, inplace=True)
    # Format the data to send as json
    data_1 = {
        "AirportCode": df_airport_mean_1.AirportCode.values.tolist(),
        "Time" : df_airport_mean_1[sample1_time].values.tolist(),
    }
    # return jsonify(json.loads(sample_data.to_json(orient='records')))
    return jsonify(data_1)

@app.route("/samples2/<sample2>")
def samples2(sample2):

    stmt = db.session.query(Flights).statement

    df = pd.read_sql_query(stmt, db.session.bind)

    if sample2 == 'TotDelayArrFlight':
        sample2_time = 'TotMinArrDelay'
    elif sample2 == "airlineDelay":
        sample2_time = "AirlineDelayTime"
    elif sample2 == "lateAircraftDelay":
        sample2_time = "LateAircraftDelayTime"
    elif sample2 == "nasDelay":
        sample2_time = "nasDelayTime"
    elif sample2 == "securityDelay":
        sample2_time = "SecurityDelayTime"
    elif sample2 == "weatherDelay":
        sample2_time = "WeatherDelayTime"

    sample2_data = df.loc[df[sample2] > 1, ["AirlineName", sample2_time]]

    df_airline_mean_2 = sample2_data.groupby('AirlineName').mean()
    # df_airport_mean_2.to_csv('test.csv')
    df_airline_mean_2 = df_airline_mean_2.reset_index()
    df_airline_mean_2.sort_values(by=sample2_time, ascending=True, inplace=True)
    # Format the data to send as json
    data_2 = {
        "AirlineName": df_airline_mean_2.AirlineName.values.tolist(),
        "Time" : df_airline_mean_2[sample2_time].values.tolist(),
    }
    # return jsonify(json.loads(sample_data.to_json(orient='records')))
    return jsonify(data_2)

@app.route("/samples3/<sample3>")
def samples3(sample3):
    stmt = db.session.query(Flights).statement
   
    df = pd.read_sql_query(stmt, db.session.bind)
   
  
    df['yrmo'] = pd.to_datetime( df['yrmo'], format='%Y%m')
    df['yrmo'] = df['yrmo'].dt.strftime('%Y-%m')
    if sample3 == 'TotDelayArrFlight':
        sample3_time = 'TotMinArrDelay'
    elif sample3 == "airlineDelay":
        sample3_time = "AirlineDelayTime"
    elif sample3 == "weatherDelay":
        sample3_time = "WeatherDelayTime"
    elif sample3 == "nasDelay":
        sample3_time = "nasDelayTime"
    elif sample3 == "securityDelay":
        sample3_time = "SecurityDelayTime"
    elif sample3 == "lateAircraftDelay":
        sample3_time = "LateAircraftDelayTime"
        
    sample3_data = df.loc[df[sample3] > 1, ["yrmo", sample3_time]]
    
    
    df_mean_3 = sample3_data.groupby('yrmo').mean()
   
    df_mean_3 = df_mean_3.reset_index()
   
    data_3 = {
        "Date": df_mean_3.yrmo.values.tolist(),
        "Time" : df_mean_3[sample3_time].values.tolist(),
    }
    
    return jsonify(data_3)

if __name__ == "__main__":
    app.run()