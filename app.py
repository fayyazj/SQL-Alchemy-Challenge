import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


import datetime
from dateutil.parser import parse

engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

measurement_df2 = pd.read_sql("select date, prcp from Measurement where date between '2016-08-23' and '2017-08-23'", conn)
station_df = pd.read_sql("select * from Station", conn)
station_list = station_df['station'].to_json(orient='records')
station281_df = pd.read_sql("select date, tobs from Measurement where station = 'USC00519281' and date between '2016-08-23' and '2017-08-23'", conn)
station281 = station281_df.to_json(orient='records')
measurement_df = pd.read_sql("select * from Measurement", conn)
last_date = measurement_df.iloc[-1]['date']

@app.route('/')
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date>/<end_date>"
    )


@app.route('/api/v1.0/precipitation')
def precipitation():
    # Calculate the date 1 year ago from last date in database
    # Query for the date and precipitation for the last year
   
    # Dict with date as the key and prcp as the value
    return jsonify(measurement_df2.to_dict(orient='records'))
   

@app.route('/api/v1.0/stations')
def stations():
    """Return a list of stations."""
    return station_list
    
@app.route('/api/v1.0/tobs')
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
    # Calculate the date 1 year ago from last date in database
    # Query the primary station for all tobs from the last year
    return station281
    
    

@app.route('/api/v1.0/<start_date>')
@app.route('/api/v1.0/<start_date>/<end_date>')
def stats(start_date=None, end_date=None):
    """Return TMIN, TAVG, TMAX."""
    if not end_date:
        end_date = last_date

        
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date>=start_date).filter(Measurement.date <= end_date).all()
    
    return jsonify(results)



if __name__ == '__main__':
    app.run()