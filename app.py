from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

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
    part_id = db.Column(db.Integer, db.ForeignKey("'Part Combinations'.part_id"), nullable=False)
    wr_time = db.relationship("WR_Times")
    track = db.relationship("Tracks")
    tune = db.relationship("Tunes")
    vehicle = db.relationship("Vehicles")
    parts_combinations = db.relationship(" 'Part Combinations' ")

class WR_Times(db.Model):
    __tablename__ = "WR_Times"
    time_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    time = db.Column(db.REAL, nullable=False)
    player = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    setup = db.session.get(Setups, 1)
    return render_template('home.html', setup=setup)

if __name__ == '__main__':
    app.run(debug=True)
