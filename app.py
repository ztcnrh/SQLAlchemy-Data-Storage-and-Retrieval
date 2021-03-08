import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine_path = 'data/hawaii.sqlite'
engine = create_engine(f'sqlite:///{engine_path}')

# Reflection
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
    """List all available api routes."""

    # Provide the date range (from the most distant to the recent date) for
    # filtering in the last two API routes
    session = Session(engine)
    start_limit = session.query(Measurement.date).filter(Measurement.date).\
                    order_by(Measurement.date).first()
    end_limit = session.query(Measurement.date).filter(Measurement.date).\
                    order_by(Measurement.date.desc()).first()

    return (
        f'Available Routes:<br/>'
        f'<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'<br/>'
        f'/api/v1.0/start<br/>'
        f'/api/v1.0/start/end<br/>'
        f'<br/>'
        f'*Please use "yyyy-mm-dd" as the date format to replace the "start" and/or "end" parameter(s) in the last two API routes in order to filter summarized temperature results based on desired date range:<br/>'
        f'The earliest date available in this dataset is {start_limit[0]}<br/>'
        f'The most recent date available in this dataset is {end_limit[0]}<br/>'
    )


@app.route('/api/v1.0/precipitation')
def prcp_by_date():
    session = Session(engine)

    """Return a list of all precipitation data and the corresponding dates"""
    # Query
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary of date and precipitation pairs
    results_dict = []
    for date, prcp in results:
        date_prcp = {}
        date_prcp['date'] = date
        date_prcp['precipitation'] = prcp
        results_dict.append(date_prcp)

    return jsonify(results_dict)


@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    """For this route I decided to wrap more information in the list of stations,
       thus now it's a list of lists of stations and their details so that
       a user of this API can see more relevant information rather than just a list
       of "USC" station codes which don't really mean anything without further context."""
    # Query all stations
    stations = session.query(Station.id,
                             Station.station,
                             Station.name).all()

    session.close()

    # Create a dictionary containing all stations' basic information
    stations_list = []
    for id, station, name in stations:
        station_info = []
        station_info.append(id)
        station_info.append(station)
        station_info.append(name)
        stations_list.append(station_info)

    return jsonify(stations_list)


@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)

    """Query the dates and temperature observations of the most active station
       for the last year of data"""
    # Query to get the query date for the time range filter
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date = most_recent_date[0].split('-')
    query_date = dt.date(int(date[0]), int(date[1]), int(date[2])) - dt.timedelta(days=365)
    
    # Query to get the most active station
    most_active_station = session.query(Station.station, func.count(Measurement.id)).\
                                        filter(Measurement.station == Station.station).\
                                        group_by(Station.station).\
                                        order_by(func.count(Measurement.id).desc()).first()[0]

    # Query the temperature data and the corresponding dates with the station and
    # the query date retrieved previously...
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
                           filter(Measurement.date >= query_date).\
                           filter(Measurement.station == most_active_station).all()

    session.close()

    # Create a dictionary of date and temperature pairs
    tobs_dict = []
    for date, tobs in tobs_results:
        date_tobs = {}
        date_tobs["date"] = date
        date_tobs["temperature"] = tobs
        tobs_dict.append(date_tobs)

    return jsonify(tobs_dict)


@app.route('/api/v1.0/<start>')
def start_date(start):
    session = Session(engine)

    """Fetch the temperature summaries derived from a date range where only
       a start date is supplied by the user;
       return a 404 if the date is out of range,
       or return an error if the dates are supplied in an unreadable format."""

    sel = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)
           ]

    if len(start) == 10:
        try:
            results = session.query(*sel).filter(Measurement.date >= start).all()
            tobs_summary_dict = {}
            for min, avg, max in results:
                tobs_summary_dict["Minimum Temperature"] = round(min, 1)
                tobs_summary_dict["Average Temperature"] = round(avg, 1)
                tobs_summary_dict["Maximum Temperature"] = round(max, 1)
            return jsonify(tobs_summary_dict)
        except:
            return jsonify({'error': f'Entered date "{start}" is likely out of range, try a smaller date.'}), 404    
    else:
        return jsonify({'error': f'Entered date "{start}" is likely not formatted correctly. Please double check if the date is in formatted in "yyyy-mm-dd".'})


@app.route('/api/v1.0/<start>/<end>')
def start_and_end_date(start, end):
    session = Session(engine)

    """Fetch the temperature summaries derived from a date range where both
       a start date and an end date are supplied by the user;
       return a 404 if the date is out of range,
       or return an error if the dates are supplied in an unreadable format."""

    sel = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)
           ]

    if len(start) == 10 and len(end) == 10:
        try:
            results = session.query(*sel).\
                              filter(Measurement.date >= start).\
                              filter(Measurement.date <= end).all()
            tobs_summary_dict = {}
            for min, avg, max in results:
                tobs_summary_dict["Minimum Temperature"] = round(min, 1)
                tobs_summary_dict["Average Temperature"] = round(avg, 1)
                tobs_summary_dict["Maximum Temperature"] = round(max, 1)
            return jsonify(tobs_summary_dict)
        except:
            return jsonify({'error': f'Entered date "{start}" or "{end}" is likely out of range, try a smaller start date or a bigger end date.'}), 404    
    else:
        return jsonify({'error': f'Either the entered date "{start}" or "{end}" is likely not formatted correctly. Please double check if the dates are in formatted in "yyyy-mm-dd".'})



if __name__ == '__main__':
    app.run(debug=True)
