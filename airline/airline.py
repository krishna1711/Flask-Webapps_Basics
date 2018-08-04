from flask import Flask,render_template,request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

app = Flask(__name__)

engine = create_engine("postgresql+psycopg2://postgres:root@localhost:5432/kritest")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html",flights=flights)


@app.route("/book",methods=["POST"])
def book():
    name = request.form.get("name")
    try:
        flight_id = request.form.get("flight_id")
    except ValueError:
        return render_template("error.html",msg = "Invalid Flight Number.")

    if db.execute("SELECT * FROM flights WHERE id=:id",{"id":flight_id}).rowcount == 0:
        return render_template("error.html",msg="No such Flight Exist")
    db.execute("INSERT INTO passengers(name,flight_id) VALUES(:name,:flight_id)",{"name":name,"flight_id":flight_id})
    db.commit()
    return render_template("sucess.html")

@app.route("/flights",methods=["POST"])##,methods=["POST"]
def flights():
    """List All Flights"""
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("flights.html",flights=flights)

@app.route("/flight/<int:flight_id>")
def flight(flight_id):
    '''List Details about Single Flight'''
    flight = db.execute("SELECT * FROM flights WHERE id=:id",{"id":flight_id}).fetchone()
    if flight is None:
        return render_template("error.html",msg="No Such Flight")

    ###Get All passengers
    passengers = db.execute("SELECT * FROM passengers WHERE flight_id=:id",{"id":flight_id}).fetchall()
    return render_template("flight.html",flight=flight,passengers=passengers)
