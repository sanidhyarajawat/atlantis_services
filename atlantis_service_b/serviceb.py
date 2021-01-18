import sqlite3
import datetime
from flask import g, Flask, request, jsonify

DATABASE = '/home/qet/ATLANTIS/atlantis_services/atlantis_service_b/service_b_database.db'
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

if __name__ == '__main__':
    app.run(port=5000,debug=True)
