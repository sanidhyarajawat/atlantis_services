import sqlite3
import datetime
from flask import g, Flask, request, jsonify

DATABASE = '/home/qet/ATLANTIS/atlantis_services/atlantis_service_a/service_a_database.db'
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/records", methods=["GET"])
def get_records():
    return {"records": query_db("select * from records")}

@app.route("/records/<record_id>", methods=["GET"])
def get_single_record(record_id):
    user = query_db('select * from records where id = ?', [record_id], one=True)
    if user is None:
        return {"error": "No record found!"}
    else:
        return {"record": user}

@app.route("/records", methods=["POST"])
def insert_record():
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    email = request.json["email"]
    pin_code = request.json["pin_code"]
    cur = get_db()
    cur.execute("INSERT INTO records (first_name, last_name, email, pin_code, timestamp) VALUES (?, ?, ?, ?, ?)", (first_name, last_name, email, pin_code, datetime.datetime.now()))
    cur.commit()
    cur.close()
    return {"message": "Record added"}

@app.route("/records/<record_id>", methods=["DELETE"])
def delete_record(record_id):
    cur = get_db()
    cur.execute("DELETE from records where id = {}".format(record_id))
    cur.commit()
    cur.close()
    return {"message": "Record removed"}

@app.route("/records/<record_id>", methods=["PUT"])
def update_record(record_id):
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    email = request.json["email"]
    pin_code = request.json["pin_code"]
    cur = get_db()
    cur.execute("UPDATE records SET first_name={}, last_name={}, email={}, pin_code={} where id = {}".format(first_name, last_name, email, pin_code, record_id))
    cur.commit()
    cur.close()
    return {"message": "Record updated"}

if __name__ == '__main__':
    app.run(port=5000,debug=True)
