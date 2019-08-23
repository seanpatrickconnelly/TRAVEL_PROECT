import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

#################################################
# Database Setup
#################################################

Base = automap_base()
# reflect the tables
engine = create_engine("sqlite:///db/airline_data.sqlite", encoding='utf8')
con = engine.connect()
Base.prepare(engine, reflect=True)
session = Session(engine)
df = pd.read_csv('db/Airline_Flights_Data.csv')
df.to_sql(name='flight_data',con=con,if_exists='append')
con.close()