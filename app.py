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
    tracks_list = ["Bottom Gear","No Skidding","Cuptown Relax","Landing Drive","Seesaw Road",
                   "Big Air","Beyond Climberdome","Legendary Apex","Trial of Fall",
                   "Trial of Courage","Trial of Balance","Forbidden Forest","Captain's Log",
                   "The Pond","Racing Wild","The Fast Lions","Sunburnt","Tumbleweeds",
                   "Road to Heck","Hills Ahead","Visions of Victory","Hollow Road",
                   "Barn Ride","Base Jump","Silo Showdown","Let It Snow","Slippery Slope",
                   "Crossroads","The Dunes","Beach Boys","Seaside","Showgrounds",
                   "Four-Wheel Park","Circuit 9","House Party","Call of the Night",
                   "Shape of Hills to Come","Factory Settings","Face Plant",
                   "Flip a Switch","Plain As Day","World's Fastest Animal","Fare You Well",
                   "Bridges And Stones","The Dip","Killing Floors","Shaft Redemption",
                   "Tired Alligators","Hangout Cave","Docked_Out","Rubberist","Heat Club",
                   "Whipclash","Fury Road","Yellow Snow","Sledhammer","Icicle Race",
                   "Fingerwoods","The Quarry","Lost In Transmission","Flipway","Deeper End",
                   "The Trench","Reef Grief","Canyon_Getaway","Racepalm","Jet Boost Holidays",
                   "Falling Crates","Magnet Madness","Take_Off","Long Road Down",
                   "Bill's Landing","Spartan Racing","Ballmer's Peak","Skid Happens",
                   "No Step on Snek","Bat Country","Through The Mountains","Gentle Escalation",
                   "Cool Descent","Topsy-Turvy","Roll With It","Switch It Up","Drive Through",
                   "Danger_Zone","A Bridge Too Far","Cliffside Way","Tricky Drive",
                   "Nose Miner"
                   ]
    vehicles_list = ["HR"]
    if request.method == 'POST':
        print("Inserting")
        
        #All form fields as variables for validation and insertion
        time=request.form["time"]
        player=request.form["player"]
        track_name=request.form["track_name"]
        tune1=request.form["tune1"]
        tune2=request.form["tune2"]
        tune3=request.form["tune3"]
        tune4=request.form["tune4"]
        tunes_list = [tune1,tune2,tune3,tune4]
        vehicle_name=request.form["vehicle_name"]
        slot1=request.form["slot1"]
        slot2=request.form["slot2"]
        slot3=request.form["slot3"]
        slot_list = [slot1,slot2,slot3]
        parts_list = ["Nitro","Fuel_Boost","Coin_Boost"]
        db.session.add_all([WR_Times(time=time, player=player),
                       Tracks(track_name=track_name),
                       Tunes(tune1=tune1,tune2=tune2,tune3=tune3,tune4=tune4),
                       Vehicles(vehicle_name=vehicle_name),
                       Parts(slot1=slot1, slot2=slot2, slot3=slot3)
        ])

        #Back end validation
        not_valid = False

        #Empty fields check
        if (
            not time or not player or not track_name or not tune1 
            or not tune2 or not tune3 or not tune4 or not vehicle_name 
            or not slot1 or not slot2 or not slot3
        ):
            print("Empty fields")
            not_valid = True

        #Valid fields check
        if track_name not in tracks_list:
            print("Not a valid track")
            not_valid = True

        for i in tunes_list:
            try:
                tune_int = int(i)
                if tune_int >= 21 or tune_int <= 0:
                    print("Not a valid tune")
                    not_valid = True
            except ValueError:
                print("Not a valid number")
                not_valid = True

        if vehicle_name not in vehicles_list:
            print("Not a valid vehicle")
            not_valid = True

        for i in slot_list:
            if i not in parts_list:
                print("Not a valid part")
                not_valid = True

        if slot1 == slot2 or slot2 == slot3 or slot1 == slot3:
            print("Duped parts")
            not_valid = True
        
        if not_valid:
            db.session.rollback()
        else:
            db.session.commit()
    return render_template('home.html',)

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
    times = WR_Times.query.all()
    tracks = Tracks.query.all()
    tunes = Tunes.query.all()
    vehicles = Vehicles.query.all()
    parts = Parts.query.all()
    return render_template('Setups.html',
                           setups=setups,
                           times=times,
                           tracks=tracks,
                           tunes=tunes,
                           vehicles=vehicles,
                           parts=parts)

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
