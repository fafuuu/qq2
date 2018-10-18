from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

topic = 'logging'
producer = KafkaProducer(bootstrap_servers=['qq2.ddnss.de:9092'])

@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        req = request.json
        vorname = req['firstname']
        nachname = req['lastname']
        matrikelnummer = req['matriculation_number']
        studiengang = req['course']
        email = req['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students(vorname, nachname, matrikelnummer, studiengang, email) VALUES (%s, %s, %s, %s, %s)", (vorname, nachname, matrikelnummer, studiengang, email))
        producer.send(topic, '{\n  "service_name": "1_Flask_1",\n  "operation": "POST",\n  "message": "Neuer Student angelegt"\n}')
        mysql.connection.commit()
        cur.close()
        return "Student angelegt"
        
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM students''')
        producer.send(topic, '{\n  "service_name": "1_Flask_1",\n  "operation": "GET",\n  "message": "Liste aller Studenten"\n}')
        rv = cur.fetchall()
        return str(rv)

@app.route('/students/<string:id>', methods=['GET', 'DELETE', 'PATCH'])
def student(id):
    cur = mysql.connection.cursor()
    if request.method == 'DELETE':
        cur.execute('''DELETE FROM students WHERE id=''' +id)
        mysql.connection.commit()
        cur.close()
        producer.send(topic, '{\n  "service_name": "1_Flask_1",\n  "operation": "DELETE",\n  "message": "Student geloescht"\n}')
        return "Student Deleted"

    elif request.method == 'PATCH':
        req = request.json
        # OLD PATCH
        #keys = req.keys()
        #attribute = keys[0]
        #val = "'" + req[attribute] + "'"
        #cur.execute("UPDATE students SET " + attribute + "= " + val + " WHERE id="+ id)
        vorname = req['firstname']
        nachname = req['lastname']
        matrikelnummer = req['matriculation_number']
        studiengang = req['course']
        email = req['email']
        cur.execute("UPDATE students SET vorname=%s, nachname=%s, matrikelnummer=%s,studiengang=%s, email=%s WHERE id=" +id, (vorname, nachname, matrikelnummer, studiengang, email) )
        mysql.connection.commit()
        cur.close()
        producer.send(topic, '{\n  "service_name": "1_Flask_1",\n  "operation": "PATCH",\n  "message": "Student aktualisiert"\n}')
        return "Student updated"

    if request.method == 'GET':
        cur.execute('''SELECT * FROM students WHERE id=''' + id)
        rv = cur.fetchall()
        producer.send(topic, '{\n  "service_name": "1_Flask_1",\n  "operation": "GET",\n  "message": "Einzelner Student"\n}')
        return str(rv)
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)