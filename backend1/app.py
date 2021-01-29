import os
from flask import Flask
from psycopg2 import connect

app = Flask(__name__)

LOCAL_HOSTNAME = os.environ["LOCAL_HOSTNAME"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PORT = 5432
POSTGRES_DB = "postgres"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "myverysecretpassword"


def query(s):
    conn = connect(host=POSTGRES_HOST,
                   port=POSTGRES_PORT,
                   dbname=POSTGRES_DB,
                   user=POSTGRES_USER,
                   password=POSTGRES_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(s)
    return conn, cursor


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    try:
        cn, cr = query("SELECT * FROM ServiceStatus WHERE status = 'AVAILABLE'")
        return {"ip": LOCAL_HOSTNAME, "services": [{"ip": ip, "status": status} for ip, status in cr.fetchall()]}
    except:
        return {"error": "Database is unavailable"}


if __name__ == "__main__":
    cn, cr = query(f"SELECT * FROM ServiceStatus WHERE ip = '{LOCAL_HOSTNAME}'")
    if cr.fetchall():
        cr.execute(f"UPDATE ServiceStatus SET status='AVAILABLE' WHERE ip = '{LOCAL_HOSTNAME}'")
    else:
        cr.execute(f"INSERT INTO ServiceStatus VALUES ('{LOCAL_HOSTNAME}', 'AVAILABLE')")
    cn.commit()
    app.run(host="0.0.0.0", port=80)
