#Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#create setup info
#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

## reflect an existing database/tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references 
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#declare flask app
app = Flask(__name__)

#flask routes
#List all routes that are available
@app.route("/")
def home():
    return (
        f"Routes List:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )





#if main run 
if __name__ == "__main__":
    app.run(debug = True)