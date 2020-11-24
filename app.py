import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>"
    )





@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    first_day=dt.date(2017,8,23)-dt.timedelta(days=365)
    results=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>= first_day).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    first_day=dt.date(2017,8,23)-dt.timedelta(days=365)
    temp_results = (
    session.query(Measurement.tobs)
    .filter(Measurement.date > first_day)
    .filter(Measurement.station == "USC00519281")
    .all()
)

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(temp_results))

    return jsonify(all_names)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def test(start = None, end = None):

    sel = [
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs),
    ]

    if not end:

    # Create our session (link) from Python to the DB
        result = session.query(*sel).\
        filter(Measurement.date >= start).all()

        all_names = list(np.ravel(result))

        return jsonify(all_names)
    
    result = session.query(*sel).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(result))
    session.close()

    return jsonify(all_names)


if __name__ == '__main__':
    app.run(debug=True)
