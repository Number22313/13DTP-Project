from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import Mapped

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/alloy/13DTP-Project/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Setups(db.Model):
    __tablename__ = "Setups"
    setup_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_id = db.Column(db.Integer, db.ForeignKey("WR_Times.time_id"), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey("Tracks.track_id"), nullable=False)
    tune_id = db.Column(db.Integer, db.ForeignKey("Tunes.tune_id"), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("Vehicles.vehicle_id"), nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey("Part Combinations.part_id"), nullable=False)
    wr_time = db.relationship("WR_Times")
    track = db.relationship("Tracks")
    tune = db.relationship("Tunes")
    vehicle = db.relationship("Vehicles")
    parts_combinations = db.relationship("Parts")

class WR_Times(db.Model):
    __tablename__ = "WR_Times"
    time_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    time = db.Column(db.REAL, nullable=False)
    player = db.Column(db.Text, nullable=False)

class Tracks(db.Model):
    __tablename__ = "Tracks"
    track_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    track_name = db.Column(db.Text, nullable=False)

class Tunes(db.Model):
    __tablename__ = "Tunes"
    tune_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    tune1 = db.Column(db.Integer, nullable=False)
    tune2 = db.Column(db.Integer, nullable=False)
    tune3 = db.Column(db.Integer, nullable=False)
    tune4 = db.Column(db.Integer, nullable=False)

class Vehicles(db.Model):
    __tablename__ = "Vehicles"
    vehicle_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    vehicle_name = db.Column(db.Text, unique=True)

class Parts(db.Model):
    __tablename__ = "Part Combinations"
    part_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    slot1 = db.Column(db.Text, nullable=False)
    slot2 = db.Column(db.Text, nullable=False)
    slot3 = db.Column(db.Text, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def Home():
    if request.method == 'POST':
        print("Inserting")
        db.session.add(WR_Times(time=request.form["time"], player=request.form["player"]),
                       Tracks(track_name=request.form["track_name"]),
                       Tunes(tune1=request.form["tune1"], tune2=request.form["tune2"],
                             tune3=request.form["tune3"], tune4=request.form["tune4"]),
                       Vehicles(vehicle_name=request.form["vehicle_name"]),
                       Parts
                )
        db.session.commit()
    return render_template('home.html')

@app.route('/Delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        print("Deleting")
        Vehicles.query.filter_by(vehicle_name=request.form["vehicle_name"]).delete()
        WR_Times.query.filter_by(time=request.form["time"]).delete()
        WR_Times.query.filter_by(player=request.form["player"]).delete()
        db.session.commit()
    return render_template('delete.html')

@app.route('/Setups')
def setups():
    setups = Setups.query.all()

    return render_template('Setups.html', setups=setups)

@app.route('/Times')
def times():
    times = WR_Times.query.all()
    return render_template('Times.html', times=times)

@app.route('/Tracks')
def tracks():
    tracks = Tracks.query.all()
    return render_template('Tracks.html', tracks=tracks)

@app.route('/Tunes')
def tunes():
    tunes = Tunes.query.all()
    return render_template('Tunes.html', tunes=tunes)

@app.route('/Vehicles')
def vehicles():
    vehicles = Vehicles.query.all()
    return render_template('Vehicles.html', vehicles=vehicles)

@app.route('/Parts')
def parts():
    parts = Parts.query.all()
    return render_template('Parts.html', parts=parts)



if __name__ == '__main__':
    app.run(debug=True)
