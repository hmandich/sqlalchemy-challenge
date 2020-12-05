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

# Create our session (link) from Python to the DB
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

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    prcp_data = session.query(measurement.date).all()
    
#create dictionary
    results_dict = {}
    for result in prcp_data:
        results_dict[result[0]] = result[1]
    # Jsonify summary
    return jsonify(results_dict)


#if main run 
if __name__ == "__main__":
    app.run(debug = True)