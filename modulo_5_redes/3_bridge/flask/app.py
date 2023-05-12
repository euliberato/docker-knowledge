import flask 
from flask import request, json, jsonify
import requests
from mysql.connector import connect, Error

app = flask.Flask(__name__)
app.config["DEBUG"] = True 

db_config = {
    'host': 'mysql_api_container',
    'user': 'root',
    'password': '',
    'database': 'flaskdocker'
}

def connect_to_database():
    try:
        connection = connect(**db_config)
        return connection
    except Error as e:
        print(e)

@app.route("/", methods=["GET"]) 

def index(): 
    data = requests.get('https://randomuser.me/api')
    return jsonify(data.json())

@app.route("/inserthost", methods=["POST"])

def inserthost():

    data = requests.get('https://randomuser.me/api').json()
    username = data['results'][0]['name']['first']

    connection = connect_to_database()
    cursor = connection.cursor()

    for item in data:
        query = """INSERT INTO users(name) VALUE(%s)""", (username)
        values = (item['name'])
        cursor.execute(query, values)

    connection.commit()
    cursor.close()
    connection.close()

    return username

if __name__ == "__main__": 
    app.run(host="0.0.0.0",debug =True, port = "5000")