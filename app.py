from flask import Flask, render_template, request, jsonify
import sqlite3 as sql

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"

#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)
#------------------------------------------------------------
#poster page
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
        return render_template("buggy-form.html", buggy = record)

    elif request.method == 'POST':
        msg=""
        warning=""
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


        # Calculate the price of the buggy:
        file_name = 'Price.csv'
        with open(file_name) as data_file:
            lines = data_file.readlines()

        name = []
        value = []

        total_cost = 0

        for line in lines[1:]:
            names, values = line.strip().split(',')
            name.append(names)
            value.append(int(values))
        calculate = [power_type, aux_power_type, hamster_booster, tyres, armour, attack]
        calculate_boolean = [fireproof, insulated, antibiotic, banging, algo]
        for c in calculate:
            if c == name:
                name = value
                total_cost += value
            print(total_cost)

        #print(f'The names are {name}')
        #print(f'The values are {value}')


        if int(qty_wheels) % 2 != 0:
            warning = "You cannot have an odd number of wheels."
        elif int(qty_tyres) < int(qty_wheels):
            warning = "You cannot have less tyres than wheels."
        elif algo == 'Buggy':
            warning = ' The race computer algorithm cannot be "Buggy".  This is a state that occurs when the racing buggy is severly damaged.'
        # Race rule: if you have non-consumable energy type then the power units must be 1
        one_power_type = ['Fusion', 'Thermo', 'Solar', 'Wind']
        for p in one_power_type:
            if power_type == p:
                power_units = 1
            elif aux_power_type == p:
                aux_power_units = 1

        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute(
                    "UPDATE buggies set qty_wheels=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?, flag_color=?, flag_pattern=?, flag_color_secondary=?, tyres=?, qty_tyres=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=?, antibiotic=?, banging=?, algo=? WHERE id=?",
                    (qty_wheels, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, DEFAULT_BUGGY_ID)
                )
                con.commit()
                msg = "Record successfully saved"
                    #msg = f"qty_weels={qty_wheels}  flag_color={flag_color}"
        except:
            con.rollback()
            msg = "error in update operation"
        finally:
            con.close()
        return render_template("updated.html", msg = msg, warning = warning)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/newspapper')
def show_bug():

    return('This is the second route!')


@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone();
    return render_template("buggy.html", buggy = record)
#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit')
def edit_buggy():
    return render_template("buggy-form.html")

#------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items()
    return jsonify({ key: val for key, val in buggies if (val != "" and val is not None) })

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
