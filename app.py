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
                   "Nose Miner","Happy Miner","A Flat Miner","Nature Calls","Chew and Run",
                   "Nectar of the Climb","Sand in Swimsuit","Tunnel Dive","The Big Dunes",
                   "Swamp Ride","Grill Bill","Happy Campers","Boarding","Carting","Overtakers",
                   "Front Window","Belter Road","Metal Gear","Braking Bad","Hairpin",
                   "Smooth Curves","Dusky Vale","Big Log Sprint","Twisted Trees","Snow Castle",
                   "Tailwind Trail","Headwind Shortcut","Like a Hawk","Deepest End",
                   "Rock and Roll","Wheeler","Deep End","Tunnel Vision","The Esses",
                   "On the Rocks","Boiling Hollow","Bone Gorge","Forgotten Highway",
                   "Frostfire Caverns","Rust Valley","Cactus Hill","Dust Valley","The Ruins",
                   "Tumbling Down","Down the Tube","Muddy Road","Cottage Road","Lonely Camper",
                   "Parking Trailers","Snappy Swamps","Bumps in the Water","Dirt Road",
                   "Danger Ahead","Highs and Lows","Get Soaked","Watery Tunnel","Don't Dive",
                   "Living on the Edge","Over the Cliff","Steep Downhill Cliff","Nowhere Road",
                   "Coconut Cove","Downtown Madness","Bumpy Ride","Rough Road",
                   "Under the Cliff","Base Camp","Crazy Climb","Top of the World",
                   "Logs and Rocks","Rock Pit","Flying Log","Tide Waves","Kid's Pool",
                   "Sandbox","Far Far Away","Hot Tarmac","The Carousel","Fast_Lane",
                   "Paradise Bay","Backwash Dash","Coral Quarrel","Thalassophobia",
                   "Access to Enjoyment","Liability Free Run","Generate Delight",
                   "Approaching Dread","Commence Fright","Spook On,Spook Off",
                   "You shall not jump","The Princess Drive","Puddle Bender","A Storm of Stumps",
                   "Special Stage One","Special Stage Two","Special Stage Three","Nightlife",
                   "Neighbourbonnet","Boost Boulevard","Jumpin' Jack Crash","Breakneck Blitz",
                   "Carppuccino","Smooth Blend","Bean 2 Tank","Dire Drive",
                   "One Does Not Simply","Ice Era","Logging In","Stumped","The Root Cause",
                   "Natural Sprinters","Let's Hunt Some Torque","Mud's Back on the Menu",
                   
                   #Adventure maps
                   "Countryside","Spring Falls","Forest","City","Mountain","Rustbucket Reef",
                   "Winter","Mines","Desert Valley","Beach","Backwater Bog","Racer Glacier",
                   "Patchwork Plant","Switchback Savanna","Gloomvale","Overspill Fun Rig",
                   "Canyon Arena","Cuptown","Sky Rock Outpost","Forest Trials","Intense City",
                   "Arena Gauntlet","Raging Winter"
                   ]
    vehicles_list = ["Hill Climber","Scooter","Bus","Hill Climber Mk2","Tractor","Motocross",
                     "Dune Buggy","Sports Car","Monster Truck","Rotator","Super Diesel",
                     "Chopper","Tank","Lowrider","Snowmobile","Monowheel","Beast",
                     "Rally Car","Formula","Muscle Car","Racing Truck","Hot Rod","CC-EV",
                     "Superbike","Supercar","Moonlander","Rock Bouncer","Hoverbike","Raider",
                     "Glider","Bolt","ATV","Offroader","Stocker"
                     ]
    parts_list = ["Magnet","Heavyweight","Wings","Rollcage","Air Control","Winter Tires",
                  "Start Boost","Wheelie Boost","Fume Boost","Flip Boost","Jump Shocks",
                  "Landing Boost","Overcharged Turbo","Afterburner","Spoiler","Thrusters",
                  "Fuel Boost","Coin Boost","Nitro"
                  ]

    if request.method == 'POST':
        insert_submit = request.form.get("insert submit")
        if insert_submit == "insert":
            print("Inserting")
            
            #All form fields as variables for validation and insertion
            not_valid = False
            time=request.form.get("time","")
            player=request.form.get("player","")
            track_name=request.form.get("track_name","")
            tune1=request.form.get("tune1","")
            tune2=request.form.get("tune2","")
            tune3=request.form.get("tune3","")
            tune4=request.form.get("tune4","")
            try:
                tune1 = int(tune1)
                tune2 = int(tune2)
                tune3 = int(tune3)
                tune4 = int(tune4)
                time = float(time)
            except ValueError:
                not_valid = True
                tune1,tune2,tune3,tune4 = 0,0,0,0
                time = 0.0
            tunes_list = [tune1,tune2,tune3,tune4]
            vehicle_name=request.form.get("vehicle_name","")
            slot1=request.form.get("slot1","")
            slot2=request.form.get("slot2","")
            slot3=request.form.get("slot3","")
            slot_list = [slot1,slot2,slot3]

            #Back end validation

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
                print("Invalid Fields")
            else:
                #Search the db for matching fields
                vehicle_query = Vehicles.query.filter_by(vehicle_name=vehicle_name).first()
                if not vehicle_query:
                    vehicle_query = Vehicles(vehicle_name=vehicle_name)
                    db.session.add(vehicle_query)

                track_query = Tracks.query.filter_by(track_name=track_name).first()
                if not track_query:
                    track_query = Tracks(track_name=track_name)
                    db.session.add(track_query)
                
                tune_query = Tunes.query.filter_by(tune1=tune1,tune2=tune2,tune3=tune3,tune4=tune4).first()
                if not tune_query:
                    tune_query = Tunes(tune1=tune1,tune2=tune2,tune3=tune3,tune4=tune4)
                    db.session.add(tune_query)
                
                parts_query = Parts.query.filter_by(slot1=slot1, slot2=slot2, slot3=slot3).first()
                if not parts_query:
                    parts_query = Parts(slot1=slot1, slot2=slot2, slot3=slot3)
                    db.session.add(parts_query)
                
                db.session.flush()
                
                #Check if they match
                setup_query = Setups.query.join(WR_Times).filter(
                    Setups.vehicle == vehicle_query,
                    Setups.track == track_query,
                    Setups.tune == tune_query,
                    Setups.parts_combinations == parts_query,
                    WR_Times.player == player
                ).first()
                
                #If there is a duplicate:
                if setup_query:
                    print("Already a setup")
                    if time < setup_query.wr_time.time:
                        print("Faster time")
                        setup_query.wr_time.time = time

                #No duplicate
                else:
                    print("Doesnt exist yet")
                    time_query = WR_Times(time=time,player=player)
                    db.session.add(time_query)
                    db.session.flush()

                    setup = Setups(
                        time_id = time_query.time_id,
                        vehicle_id = vehicle_query.vehicle_id,
                        track_id = track_query.track_id,
                        tune_id = tune_query.tune_id,
                        part_id = parts_query.part_id
                    )
                    db.session.add(setup)

                db.session.commit()
                print("Inserted")

    return render_template('home.html',
                           tracks_list=tracks_list,
                           vehicles_list=vehicles_list,
                           parts_list=parts_list,
                           
                           )

@app.route('/Delete', methods=['GET', 'POST'])
def delete():
    if request.method == "POST":
        delete_submit = request.form.get("delete submit")
        print(delete_submit)
        if delete_submit == "delete":
            setup = request.form.get("setup")
            print("Found Setup "+ setup)

            #delete the setup if it exists
            if setup:
                setup_id = Setups.query.get(int(setup))
                db.session.delete(setup_id)
                print("Deleted "+ setup)
                db.session.commit()
    setups = Setups.query.all()
    return render_template('delete.html',setups=setups)

@app.route('/Setups', methods=['GET', 'POST'])
def setups():
    setup = []

    setups = Setups.query.all()
    times = WR_Times.query.all()
    tracks = Tracks.query.all()
    tunes = Tunes.query.all()
    vehicles = Vehicles.query.all()
    parts = Parts.query.all()

    if request.method == 'POST':
        search_bar = request.form.get("search bar")

        #Convert the search to integer and float for tunes and times
        try:
            real = float(search_bar)
        except ValueError:
            real = None
        
        try:
            integer = int(search_bar)
        except ValueError:
            integer = None

        #Search and filter data
        if search_bar != "":
            print("Searching for: "+search_bar)
            setup = Setups.query.filter((Setups.track.has(Tracks.track_name == search_bar))|
                                            (Setups.wr_time.has((WR_Times.time == real)|
                                                                (WR_Times.player == search_bar)))|
                                            (Setups.tune.has((Tunes.tune1 == integer)|
                                                             (Tunes.tune2 == integer)|
                                                             (Tunes.tune3 == integer)|
                                                             (Tunes.tune4 == integer)))|
                                            (Setups.vehicle.has(Vehicles.vehicle_name == search_bar))|
                                            (Setups.parts_combinations.has((Parts.slot1 == search_bar)|
                                                                           (Parts.slot2 == search_bar)|
                                                                           (Parts.slot3 == search_bar)))
                                            ).all()
    return render_template('Setups.html',
                           setups=setups,
                           times=times,
                           tracks=tracks,
                           tunes=tunes,
                           vehicles=vehicles,
                           parts=parts,
                           setup=setup)

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
