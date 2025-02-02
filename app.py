from flask import Flask, render_template, request, jsonify, redirect, session
import sqlite3 as sql
from random import Random
import unittest

# app - The flask application where all the magical things are configured.
app = Flask(__name__)
app.secret_key = 'kl1rm59wr23r1'

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"

#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    username = request.cookies.get('username')
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# poster page
#------------------------------------------------------------
@app.route('/poster')
def poster():
    return render_template('poster.html')
#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchone();
        return render_template("buggy-form.html", buggy = None)

    elif request.method == 'POST':
        msg=""
        qty_wheels = request.form['qty_wheels']
        power_type = request.form['power_type']
        power_units = request.form['power_units']
        aux_power_type = request.form['aux_power_type']
        aux_power_units = request.form['aux_power_units']
        hamster_booster = request.form['hamster_booster']
        flag_color = request.form['flag_color']
        flag_pattern = request.form['flag_pattern']
        flag_color_secondary = request.form['flag_color_secondary']
        tyres = request.form['tyres']
        qty_tyres = request.form['qty_tyres']
        armour = request.form['armour']
        attack = request.form['attack']
        qty_attacks = request.form['qty_attacks']
        fireproof = request.form['fireproof']
        insulated = request.form['insulated']
        antibiotic = request.form['antibiotic']
        banging = request.form['banging']
        algo = request.form['algo']
        buggy_id = request.form['id']

# Validation data
        motive_power = ['Fusion', 'Thermo', 'Solar', 'Wind']
        type_power = [power_type, aux_power_type]
        units = [power_units, aux_power_units]

        if power_type in motive_power:
            power_units = 1

        if aux_power_type in motive_power:
            aux_power_units = 1


        name = ['Petrol', 'Fusion', 'Steam', 'Bio', 'Electric', 'Rocket', 'Hamster', 'Thermo', 'Solar', 'Wind']
        value = [4, 400, 3, 5, 20, 16, 3, 300, 40, 20]

        tyres_type = ['Knobbly', 'Slick', 'Steelband', 'Reactive', 'Maglev']
        tyres_price = [15, 10, 20, 40, 50]

        armour_type = ['Wood', 'Aluminium', 'Thinsteel', 'Thicksteel', 'Titanium']
        armour_cost = [40, 200, 100, 200, 290]

        extra = [fireproof, insulated, antibiotic, banging]
        extra_cost = [70, 100, 90, 42]

        capabilities = ['Spike', 'Flame', 'Charge', 'Biohazard']
        capabilities_price = [5, 20, 28, 30]
        total_cost = 0

# Calculate the price of the buggy based on the input
        if aux_power_type != 'Hamster':
            hamster_booster = 0
        if power_type != 'Hamster':
            hamster_booster = 0
        if aux_power_type == 'None':
            aux_power_units = 0
        else:
            total_cost += int(hamster_booster)*5

        for c, cp in zip(capabilities, capabilities_price):
            if attack in c:
                total_cost += cp

        for e, ec in zip(extra, extra_cost):
            if e == 'True':
                total_cost += ec
        for at, ac in zip(armour_type, armour_cost):
            if armour in at:
                total_cost += ac*((int(qty_wheels))-4)*10/100 + ac

        for t, p in zip(tyres_type, tyres_price):
            if tyres in t:
                total_cost += int(qty_tyres)*p

        for a, b in zip(name, value):
            if power_type in a:
                total_cost += int(b)*int(power_units)
            elif aux_power_type in a:
                    total_cost += int(b)*int(aux_power_units)

        print(f'{total_cost} is the total cost of the buggy')

        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                if buggy_id:
                    cur.execute(
                        "UPDATE buggies set qty_wheels=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?, flag_color=?, flag_pattern=?, flag_color_secondary=?, tyres=?, qty_tyres=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=?, antibiotic=?, banging=?, algo=?, total_cost=? WHERE id=?",
                        (qty_wheels, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, total_cost, buggy_id)
                    )
                else:
                    cur.execute(
                        "INSERT INTO buggies (qty_wheels, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, total_cost) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (qty_wheels, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, total_cost,)
                    )
                con.commit()
                msg = "Record successfully saved"
        except:
            con.rollback()
            msg = "error in update operation"
        finally:
            con.close()
            return render_template("updated.html", msg = msg)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    records = cur.fetchall();
    if records == None:
        print('No buggy available')
    else:
        return render_template("buggy.html", buggies = records)
#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit/<buggy_id>')
def edit_buggy(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=?", (buggy_id,))
    record = cur.fetchone();
    return render_template("buggy-form.html", buggy=record)

#------------------------------------------------------------
# delete route
#------------------------------------------------------------
@app.route('/delete/<buggy_id>', methods=['POST', 'GET'])
def delete_buggy(buggy_id):
    if request.method == 'POST':
        con = sql.connect(DATABASE_FILE)
        con.execute("DELETE FROM buggies WHERE id=?", (buggy_id,))
        con.commit()
        return redirect("/buggy")
    elif request.method == 'GET':
        return redirect('/')
#------------------------------------------------------------
# log in route
#------------------------------------------------------------
#session['email'] = value
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        for key, value in request.form.items():
            print(f'{key}: {value}')
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return render_template('index.html')

    return render_template('login.html')

#------------------------------------------------------------
# log out route
#------------------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

#------------------------------------------------------------
# sign up route
#------------------------------------------------------------
@app.route('/signup')
def signup():
    return render_template('signup.html')
#------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
#------------------------------------------------------------
# json initial page
#------------------------------------------------------------
@app.route('/json')
def get_json():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    records = cur.fetchall();
    return render_template("json.html", buggies = records)
#------------------------------------------------------------
# json for a certain buggy
#------------------------------------------------------------
@app.route('/json/<buggy_id>')
def summary(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (buggy_id,))

    buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items()
    return jsonify({ key: val for key, val in buggies if (val != "" and val is not None) })

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
    unittest.main()
