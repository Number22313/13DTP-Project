from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_
from sqlalchemy.orm import aliased

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/alloy/13DTP-Project/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'temporary_secret_key'
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


@app.errorhandler(404)
def error(a):
    return render_template('error.html')


def wr_subquery():
    #World Record setups
    Setup_subquery = aliased(Setups)
    return Setups.query.join(WR_Times).filter(WR_Times.time == (db.session.query(func.min(WR_Times.time))
                                                                .join(Setup_subquery, WR_Times.time_id == Setup_subquery.time_id)
                                                                .filter(Setup_subquery.track_id == Setups.track_id,
                                                                        Setup_subquery.vehicle_id == Setups.vehicle_id)
                                                                .scalar_subquery()))


@app.before_request
def settings_menu():
    rpp_options = {'5','10','20','30','40'}
    rpp = request.form.get('rows_per_page')
    theme = request.form.get('theme')
    if 'theme' not in session:
            session['theme'] = 'dark'
    
    if request.method == 'POST' and 'Save' in request.form:
        #validation
        if theme and theme == 'dark':
            session['theme'] = 'dark'
        else:
            session['theme'] = 'light'

        if rpp in rpp_options:
            session['rows_per_page'] = rpp
        else:
            session['rows_per_page'] = '10'
        return redirect(request.referrer or url_for('Home'))


@app.route('/', methods=['GET', 'POST'])
def Home():
    setups_count = Setups.query.count()
    total_parts = Parts.query.count()
    unique_players = set()
    for i in WR_Times.query.all():
        unique_players.add(i.player)
    
    total_players = 0
    for p in unique_players:
        total_players += 1

    fastest_times = Setups.query.join(WR_Times).order_by(WR_Times.time.asc()).all()
    return render_template('home.html',
                           active_page='Home',
                           setups_count=setups_count,
                           total_parts=total_parts,
                           total_players=total_players,
                           fastest_times=fastest_times)


@app.route('/Setups', methods=['GET', 'POST'])
def setups():
    insert_errors = []
    if request.method == 'POST':
        if 'setup_delete' in request.form:
            setup_delete = request.form.get('setup_delete')
            try:
                setup_delete = int(setup_delete)
                Setups.query.filter(Setups.setup_id == setup_delete).delete()
                db.session.commit()
            except ValueError:
                insert_errors.append(f"{setup_delete} is not a valid id")
        
        if 'insert' in request.form:
            insert_submit = request.form.get("insert")
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
                if (not time or not player or not track_name or not vehicle_name 
                    or not slot1 or not slot2 or not slot3):
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

                for o in tunes_list:
                    if not o:
                        insert_errors.append(f"Not all tunes fields are full")
                        not_valid=True
                    else:
                        try:
                            tune_int = int(o)
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
                
                if len(player) >= 16:
                    insert_errors.append(f"{player} is not a real player")
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
    all_setups = Setups.query.all()
    return render_template('Setups.html',
                           active_page='setups',
                           setups=all_setups,
                           tracks_list=tracks_list,
                           vehicles_list=vehicles_list,
                           parts_list=parts_list,
                           insert_errors=insert_errors)


@app.route('/Search', methods=['GET', 'POST'])
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
    wr_checked = request.args.get("wr_checked") or None
    player_filter = request.args.getlist("player_filter") or None
    track_filter = request.args.getlist("track_filter") or None
    vehicle_filter = request.args.getlist("vehicle_filter") or None
    
    players_options = []
    for c in (db.session.query(WR_Times.player).join(Setups).distinct().all()):
        players_options.append(c[0])
        

    search_bar = request.args.get("search_bar") or None
    
    setup = Setups.query.join(WR_Times).join(Vehicles).join(Tracks).join(Tunes).join(Parts).order_by(WR_Times.time.asc())

    #Filter setups with actual inputs
    if vehicle_filter:
        vehicle = [v for v in vehicle_filter if v in vehicles_list]
        setup = setup.filter(Vehicles.vehicle_name.in_(vehicle))

        vehicle_invalid = [v for v in vehicle_filter if v not in vehicles_list]
        for v in vehicle_invalid:
            result_errors.append(f"{v} is not a valid vehicle")
    
    if time:
        try:
            time = float(time)
            if time > 0:
                setup = setup.filter(WR_Times.time == time)
            else:
                result_errors.append(f"time must be greater than 0")
        except ValueError:
            result_errors.append(f"{time} is not a number")
    
    if player_filter:
        player = [p for p in player_filter if p in players_options]
        setup = setup.filter(WR_Times.player.in_(player))

        player_invalid = [p for p in player_filter if p not in players_options]
        for p in player_invalid:
            result_errors.append(f"{p} player has no setups")

    if track_filter:

        track = [t for t in track_filter if t in tracks_list]
        setup = setup.filter(Tracks.track_name.in_(track))

        track_invalid = [t for t in track_filter if t not in tracks_list]
        for t in track_invalid:
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

    master_list_lower = {}
    for z in (tracks_list+vehicles_list+parts_list+players_options):
        master_list_lower[z.lower()] = z

    if search_bar:
        #Search and filter data

        #Search word matching (2 words to X words)
        loop_index = 0
        search_split = search_bar.strip().split()
        filter_match = []
        length = len(search_split)
        while loop_index < len(search_split):
            match = False
            for search_length in range(length,1,-1):
                if loop_index + search_length <= len(search_split):
                    word = " ".join(search_split[loop_index:loop_index+search_length])
                    if word.lower() in (master_list_lower):
                        loop_index += search_length
                        match = True
                        filter_match.append(master_list_lower[word.lower()])
                        break

            #1 word match
            if not match:
                filter_match.append(search_split[loop_index])
                loop_index += 1


        #Filter results by search

        for c in filter_match:
            search_filter = [Tracks.track_name.ilike(c),
                      Vehicles.vehicle_name.ilike(c),
                      WR_Times.player.ilike(c),
                      Parts.slot1.ilike(c),
                      Parts.slot2.ilike(c),
                      Parts.slot3.ilike(c)]

            try:
                search_time = float(c)
                if search_time > 0:
                    search_filter.append(WR_Times.time == search_time)
                else:
                    result_errors.append(f"(search) {search_time} cannot be negative")
            except ValueError:
                pass

            try:
                search_tune = int(c)
                if search_tune > 0:
                    search_filter.extend([Tunes.tune1 == search_tune,
                                Tunes.tune2 == search_tune,
                                Tunes.tune3 == search_tune,
                                Tunes.tune4 == search_tune])
                else:
                    result_errors.append(f"(search) {search_tune} cannot be negative")
            except ValueError:
                pass

            setup = setup.filter(or_(*search_filter))

    #Filter results for wrs
    if wr_checked:
        setup = wr_subquery()
    
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
                           active_page='search',
                           tracks_list=tracks_list,
                           vehicles_list=vehicles_list,
                           parts_list=parts_list,
                           search_bar=search_bar or "",
                           result=result,
                           players=players_options,
                           result_errors=result_errors)


@app.route('/Leaderboards', methods=['GET', 'POST'])
def leaderboards():
    all_setups = Setups.query.all()

    #All players with WRs and number of WRs
    wr = wr_subquery().all()

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
                           active_page='leaderboards',
                           player_wr_count=player_wr_count,
                           parts_count=parts_count)



if __name__ == '__main__':
    app.run(debug=True)
