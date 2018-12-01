import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Create our session (link) from Python to the DB
session = Session(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
   return ( 
       f"Welcome to the Hawaii Climate Analysis API!<br/>"
       f"Available Routes:<br/>"
       f"/api/v1.0/precipitation<br/>"
       f"/api/v1.0/stations<br/>"
       f"/api/v1.0/tobs<br/>"
       f"/api/v1.0/temp/start_date<br/>"
       f"/api/v1.0/temp/start_date/end_date<br/>"
       f"/api/v1.0/temp/enter_date<br/>"
   )

@app.route("/api/v1.0/precipitation")
def precipitation():

    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precip_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= start_date).all()

   # Convert results into a dictionary of precipitation (tutor helped me set up the date and dictionary with loop)
    precip = {date: prcp for date, prcp in precip_results}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():

   station_results = session.query(Station.station).all()

   # Convert results into a list of stations
   stations = list(np.ravel(station_results))
   return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
   start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   
   tobs_results = session.query(Measurement.date, Measurement.tobs).\
       filter(Measurement.date >= start_date).all()

   # Convert results into a list of tobs
   temp = list(np.ravel(tobs_results))
   return jsonify(temp)

# Return temperature (min-ave-max : mam) for a specific date range given start_date (>= start_date) 
@app.route("/api/v1.0/temp/<start_date>")

def temp_start(start_date):

    """TMIN, TAVG, and TMAX for a list of dates.
    Args:
        start_date (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVE, and TMAX
    """

    mam_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()
    
    # Convert results into a list of min, ave, max temps for >=start_date
    mam_temp_start = list(np.ravel(mam_temp_results))
    return jsonify(mam_temp_start)

# temperature (min-ave-max : mam) for a specific date range (provide start and end date) 
@app.route("/api/v1.0/temp/<start_date>/<end_date>")

def temp_daterange(start_date,end_date):

    """TMIN, TAVG, and TMAX for a list of dates.
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVE, and TMAX
    """

    mam_temp_dr_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    # Convert results into a list of min, ave, max temps for date range with specific start_date and end_date
    mam_temp_start_end = list(np.ravel(mam_temp_dr_results))
    return jsonify(mam_temp_start_end)

# temperature (min-ave-max : mam) for a specific date (did this to test my code for start date and date range).
@app.route("/api/v1.0/temp/<enter_date>")

def temp_date(enter_date):

    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVE, and TMAX
    """

    mam_temp_date_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date == enter_date).all()
    
    # Convert results into a list of min, ave, max temps for a specific date
    mam_temp_date = list(np.ravel(mam_temp_date_results))
    return jsonify(mam_temp_date)

if __name__ == '__main__':
   app.run()