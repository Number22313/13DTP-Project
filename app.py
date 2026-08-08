from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import aliased

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/alloy/13DTP-Project/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

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


class Setups(db.Model):
    __tablename__ = "Setups"
    setup_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_id = db.Column(db.Integer, db.ForeignKey("WR_Times.time_id"), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey("Tracks.track_id"), nullable=False)
    tune_id = db.Column(db.Integer, db.ForeignKey("Tunes.tune_id"), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("Vehicles.vehicle_id"), nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey("Part Combinations.part_id"), nullable=False)
    wr_time = db.relationship("WR_Times", back_populates="setups")
    track = db.relationship("Tracks", back_populates="setups")
    tune = db.relationship("Tunes", back_populates="setups")
    vehicle = db.relationship("Vehicles", back_populates="setups")
    parts_combinations = db.relationship("Parts", back_populates="setups")

class WR_Times(db.Model):
    __tablename__ = "WR_Times"
    time_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    time = db.Column(db.REAL, nullable=False)
    player = db.Column(db.Text, nullable=False)
    setups = db.relationship("Setups", back_populates="wr_time")

class Tracks(db.Model):
    __tablename__ = "Tracks"
    track_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    track_name = db.Column(db.Text, nullable=False)
    setups = db.relationship("Setups", back_populates="track")

class Tunes(db.Model):
    __tablename__ = "Tunes"
    tune_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    tune1 = db.Column(db.Integer, nullable=False)
    tune2 = db.Column(db.Integer, nullable=False)
    tune3 = db.Column(db.Integer, nullable=False)
    tune4 = db.Column(db.Integer, nullable=False)
    setups = db.relationship("Setups", back_populates="tune")

class Vehicles(db.Model):
    __tablename__ = "Vehicles"
    vehicle_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    vehicle_name = db.Column(db.Text, unique=True)
    setups = db.relationship("Setups", back_populates="vehicle")

class Parts(db.Model):
    __tablename__ = "Part Combinations"
    part_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    slot1 = db.Column(db.Text, nullable=False)
    slot2 = db.Column(db.Text, nullable=False)
    slot3 = db.Column(db.Text, nullable=False)
    setups = db.relationship("Setups", back_populates="parts_combinations")


@app.route('/', methods=['GET', 'POST'])
def Home():
    insert_errors = []
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
            except (TypeError,ValueError):
                not_valid = True
                tune1,tune2,tune3,tune4 = 0,0,0,0
            tunes_list = [tune1,tune2,tune3,tune4]
            vehicle_name=request.form.get("vehicle_name","")
            slot_list = sorted([request.form.get("slot1",""),
                                request.form.get("slot2",""),
                                request.form.get("slot3","")
                                ])
            slot1,slot2,slot3 = slot_list
            print(f"{slot_list}")

            #Back end validation

            #Empty fields check
            if (not time or not player or not track_name or not tune1 
                or not tune2 or not tune3 or not tune4 or not vehicle_name 
                or not slot1 or not slot2 or not slot3):
                insert_errors = []
                insert_errors.append("Not all fields are filled")
                not_valid = True


            if track_name not in tracks_list:
                insert_errors.append(f"{track_name} is not a valid track")
                not_valid = True
            
            if time:
                try:
                    time = float(time)
                    print(time)
                    if time < 0:
                        insert_errors.append(f"{time} is not a valid time")
                        not_valid = True
                except(ValueError,TypeError):
                    insert_errors.append(f"{time} is not a number")
                    not_valid = True

            for i in tunes_list:
                try:
                    tune_int = int(i)
                    if tune_int >= 21 or tune_int <= 0:
                        insert_errors.append(f"{tune_int} is not a valid tune")
                        not_valid = True
                except ValueError:
                    insert_errors.append(f"{tune_int} is not a number")
                    not_valid = True

            if vehicle_name not in vehicles_list:
                insert_errors.append(f"{vehicle_name} is not a valid vehicle")
                not_valid = True

            for i in slot_list:
                if i not in parts_list:
                    insert_errors.append(f"{i} is not a valid part")
                    not_valid = True

            if slot1 == slot2 or slot2 == slot3 or slot1 == slot3:
                insert_errors.append("Duped parts")
                not_valid = True
            
            if not_valid:
                insert_errors.append("Invalid Fields")
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

                player_query = WR_Times.query.filter(WR_Times.player.ilike(player)).first()
                if player_query:
                    player = player_query.player
                
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
                        insert_errors.append("Updated")
                        setup_query.wr_time.time = time

                #No duplicate
                elif not setup_query:
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
                    insert_errors.append("Inserted")

                db.session.commit()

    return render_template('home.html',
                           tracks_list=tracks_list,
                           vehicles_list=vehicles_list,
                           parts_list=parts_list,
                           insert_errors=insert_errors
                           )

@app.route('/Delete', methods=['GET', 'POST'])
def delete():
    if request.method == "POST":
        delete_submit = request.form.get("delete submit")
        if delete_submit == "delete":
            form = request.form.get("setup")
            print(f"Found Setup {form}")
            if form:
                setup = Setups.query.get(form)
                #delete the setup if it exists
                if setup:
                    db.session.delete(setup)
                    db.session.flush()
                    old_player = WR_Times.query.filter(~WR_Times.setups.any()).all()
                    for i in old_player:
                        print(f"Deleted unused player: {i.player}")
                        db.session.delete(i)
                    print(f"Deleted {setup}")
                    db.session.commit()
    all_setups = Setups.query.all()
    return render_template('delete.html',setups=all_setups)

@app.route('/Setups', methods=['GET', 'POST'])
def setups():
    all_setups = Setups.query.all()
    times = WR_Times.query.all()
    tracks = Tracks.query.all()
    tunes = Tunes.query.all()
    vehicles = Vehicles.query.all()
    parts = Parts.query.all()
    return render_template('Setups.html',
                           setups=all_setups,
                           times=times,
                           tracks=tracks,
                           tunes=tunes,
                           vehicles=vehicles,
                           parts=parts)

@app.route('/Times')
def times():
    times = WR_Times.query.all()
    return render_template('Times.html', times=times)

@app.route('/Search')
def search():
    setup = []
    result_errors = []
    wr_setups = []
    time = request.args.get("time") or None
    tune1 = request.args.get("tune1") or None
    tune2 = request.args.get("tune2") or None
    tune3 = request.args.get("tune3") or None
    tune4 = request.args.get("tune4") or None
    slot1 = request.args.get("slot1") or None
    slot2 = request.args.get("slot2") or None
    slot3 = request.args.get("slot3") or None
    tunes = [(tune1, Tunes.tune1),
            (tune2, Tunes.tune2),
            (tune3, Tunes.tune3),
            (tune4, Tunes.tune4)]
    wr_checked = request.args.get("wr_checked")
    player_filter = request.args.getlist("player_filter")
    track_filter = request.args.getlist("track_filter")
    vehicle_filter = request.args.getlist("vehicle_filter")
    
    players_options = []
    for c in (db.session.query(WR_Times.player).join(Setups).distinct().all()):
        players_options.append(c[0])
        

    search_bar = request.args.get("search_bar") or None
    
    setup = Setups.query.join(WR_Times).join(Vehicles).join(Tracks).join(Tunes).join(Parts).order_by(WR_Times.time.asc())

    #Filter setups with actual inputs
    if vehicle_filter:
        for v in vehicle_filter:
            if v in vehicles_list:
                setup = setup.filter(Vehicles.vehicle_name == v)
            else:
                result_errors.append(f"{v} is not a valid vehicle")
    
    if time:
        try:
            time = int(time)
            if time > 0:
                setup = setup.filter(WR_Times.time == time)
            else:
                result_errors.append(f"time must be greater than 0")
        except ValueError:
            result_errors.append(f"{time} is not a number")
    
    if player_filter:
        for p in player_filter:
            if p in players_options:
                setup = setup.filter(WR_Times.player == p)
            else:
                result_errors.append(f"{p} has no setups")

    if track_filter:
        for t in track_filter:
            if t in track_filter:
                setup = setup.filter(Tracks.track_name == t)
            else:
                result_errors.append(f"{t} is not a valid track")
    
    for value,column in tunes:
        if value:
            try:
                value = int(value)
                if 21 > value > 0:
                    setup = setup.filter(column == value)
                else:
                    result_errors.append(f"{value} is not between 1 and 20")
            except ValueError:
                result_errors.append(f"{value} is not an integer")
            
    if slot1:
        if slot1 in parts_list:
            setup = setup.filter((Parts.slot1 == slot1)|
                                (Parts.slot2 == slot1)|
                                (Parts.slot3 == slot1))
        else:
            result_errors.append(f"{slot1} is not a valid part")
    
    if slot2:
        if slot2 in parts_list:
            setup = setup.filter((Parts.slot1 == slot2)|
                                (Parts.slot2 == slot2)|
                                (Parts.slot3 == slot2))
        else:
            result_errors.append(f"{slot2} is not a valid part")
        
    if slot3:
        if slot3 in parts_list:
            setup = setup.filter((Parts.slot1 == slot3)|
                                (Parts.slot2 == slot3)|
                                (Parts.slot3 == slot3))
        else:
            result_errors.append(f"{slot3} is not a valid part")

    if search_bar:
        #Convert the search to an integer and float
        try:
            real = float(search_bar)
        except ValueError:
            real = None

        try:
            integer = int(search_bar)
        except ValueError:
            integer = None

        #Search and filter data
        print("Searching for: "+search_bar)
        setup = setup.filter((Setups.track.has(Tracks.track_name.ilike(search_bar)))|
                                        (Setups.wr_time.has((WR_Times.time == real)|
                                                            (WR_Times.player.ilike(search_bar))))|
                                        (Setups.tune.has((Tunes.tune1 == integer)|
                                                            (Tunes.tune2 == integer)|
                                                            (Tunes.tune3 == integer)|
                                                            (Tunes.tune4 == integer)))|
                                        (Setups.vehicle.has(Vehicles.vehicle_name.ilike(search_bar)))|
                                        (Setups.parts_combinations.has((Parts.slot1.ilike(search_bar))|
                                                                        (Parts.slot2.ilike(search_bar))|
                                                                        (Parts.slot3.ilike(search_bar))))
                                        )
    #Filter results for wrs
    if wr_checked:
        Setup_subquery = aliased(Setups)

        setup = (setup.filter(WR_Times.time == (db.session.query(func.min(WR_Times.time))
                                                                .join(Setup_subquery, WR_Times.time_id == Setup_subquery.time_id)
                                                                .filter(Setup_subquery.track_id == Setups.track_id,
                                                                        Setup_subquery.vehicle_id == Setups.vehicle_id)
                                                                .scalar_subquery())))
    
    #All or nothing
    if result_errors:
        result = []
    else:
        result = setup.all()

        if wr_checked:
            for i in result:
                wr_setups.append(int(i.setup_id))
            print(f"{wr_setups}")
    
    return render_template('Search.html',
                           tracks_list=tracks_list,
                           vehicles_list=vehicles_list,
                           parts_list=parts_list,
                           search_bar=search_bar or "",
                           result=result,
                           players=players_options,
                           result_errors=result_errors)

@app.route('/Leaderboards')
def leaderboards():
    all_setups = Setups.query.all()

    #WR
    Setup_subquery = aliased(Setups)

    wr = (Setups.query.join(WR_Times).filter(WR_Times.time == (db.session.query(func.min(WR_Times.time))
                                                            .join(Setup_subquery, WR_Times.time_id == Setup_subquery.time_id)
                                                            .filter(Setup_subquery.track_id == Setups.track_id,
                                                                    Setup_subquery.vehicle_id == Setups.vehicle_id)
                                                            .scalar_subquery())).all())
    wr_count = []
    for z in wr:
        wr_count.append(z.wr_time.player)

    wr_count_lower = []
    for x in wr_count:
        wr_count_lower.append(x.lower())

    player_wr_count = []
    unique_players = set()

    for i in wr_count:
        player = i.lower()
        if player not in unique_players:
            wrs = wr_count_lower.count(player)
            player_wr_count.append((wrs, i))
            unique_players.add(player)

    player_wr_count.sort(reverse=True)

    #most used parts
    all_parts = []
    for a in all_setups:
        all_parts.append(a.part_id)

    parts_count = []
    unique_parts = set(all_parts)
    for p in unique_parts:
        count = all_parts.count(p)
        parts_row = Parts.query.get(p)
        parts_count.append((count, p, parts_row))
    parts_count.sort(reverse=True)

    return render_template('Leaderboards.html',
                           player_wr_count=player_wr_count,
                           parts_count=parts_count)




if __name__ == '__main__':
    app.run(debug=True)
