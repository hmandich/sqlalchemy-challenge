#Dependencies
#typical python modules 
import datetime as dt
import numpy as np
import pandas as pd
#sqlalchemy modules
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#flask module 
from flask import Flask, jsonify


#Setup SQLAlchemy 
#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

##reflect an existing database/tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references 
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB - I know it is best practice to run sessions inside routes but I couldn't get all them to work
session = Session(engine)

#flast setup - declare flask app
app = Flask(__name__)

#Build routes
#List all routes that are available
@app.route("/")
def home():
    return (
        f"Step 2 - Climate App<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#return particitation date for last year
@app.route("/api/v1.0/precipitation")
def precipitation():
 
    prcp_data = session.query(func.strftime("%Y-%m-%d", measurement.date), measurement.prcp).\
        filter(func.strftime("%Y-%m-%d", measurement.date) >= "2016-08-23").all()
    
    prcp_results = {}
    for result in prcp_data:
        prcp_results[result[0]] = result[1]

    return jsonify(prcp_results)

#station route -  returns all stations
@app.route("/api/v1.0/stations")
def stations():

    stations_query = session.query(station).all()

     #create a list to pull all data into dictiornay 
    stations_results = []
    for s in stations_query:
        station_dt = {}
        station_dt["station"] = s.station
        station_dt["name"] = s.name
        station_dt["latitude"] = s.latitude
        station_dt["longitude"] = s.longitude
        station_dt["elevation"] = s.elevation
        stations_results.append(station_dt)

    return jsonify(stations_results)

#tobs route -  returns tobs for the most active station from last year - USC00519281
@app.route("/api/v1.0/tobs")
def tobs():

    #get temperature measurements for last year
    temp_obsv = session.query(measurement.date,measurement.tobs).filter(measurement.station=="USC00519281").\
    filter(func.strftime("%Y-%m-%d",measurement.date) >= "2016-08-23").all()

    #create list of dictionaries (one for each observation)
    tobs_results = []
    for t in temp_obsv:
        tobs_dt = {}
        tobs_dt["date"] = t.date
        tobs_dt["tobs"] = t.tobs
        tobs_results.append(tobs_dt)

    return jsonify(tobs_results)

#start date - accepects start date as parameter, returns min, max and avg temp for that date
@app.route("/api/v1.0/<start>")
def start(start):

    #set up input
    start_date =dt.datetime.func.strftime("%Y-%m-%d")

    temperatures = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
    filter(measurement.date >=start_date).all()

    summary_stats = list(np.ravel(temperatures))

    return jsonify(summary_stats)

#start and end route -  accepects start and end date as parameter, returns min, max and avg temp for that date
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
	# Set input
	start = dt.datetime.strptime(start,"%Y-%m-%d")
	End = dt.datetime.strptime(end,"%Y-%m-%d")

	# Query Min, Max, and Avg based on dates
	temperatures_2 = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
    filter(measurement.date.between(start,end).all()
	
	#summary_stats_2 = list(np.ravel(temperatures_2))

	# Jsonify summary
	return jsonify(summary_stats_2)

#close query
session.close()  

#if main run 
if __name__ == "__main__":
    app.run(debug = True)