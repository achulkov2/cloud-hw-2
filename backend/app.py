import os
from flask import Flask
from psycopg2 import connect

app = Flask(__name__)

LOCAL_HOSTNAME = os.environ['LOCAL_HOSTNAME']

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    try:
        conn = connect(host='192.168.10.15', port=5432, dbname='postgres', user='postgres', password='myverysecretpassword')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ServiceStatus')
        res = cursor.fetchall()
        response = {
            'services': [{'ip': ip, 'status': status} for ip, status in res]
        }
    except:
        response = {'error': 'Database is unavailable'}
    return response

if __name__ == '__main__':
    conn = connect(host='192.168.10.15', port=5432, dbname='postgres', user='postgres', password='myverysecretpassword')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM ServiceStatus WHERE ip = "{LOCAL_HOSTNAME}"')
    if cursor.fetchall():
        cursor.execute(f'UPDATE ServiceStatus SET status="AVAILABLE" WHERE ip = "{LOCAL_HOSTNAME}"')
    else:
        cursor.execute(f'INSERT INTO ServiceStatus VALUES ("{LOCAL_HOSTNAME}", "AVAILABLE")')
    cursor.commit()
    app.run(host='0.0.0.0', port=80)
