# QQ2 Dokumenation
Hier ist die Vorgehensweise der Bearbeitung des QQ2 Projektes dokumentiert.

**Wichtig damit die Dummy Daten geladen werden
## Installation

Python ist standardmäßig auf Ubuntu installiert

Flask installieren:
```sh
sudo apt-get install pip
pip install flask
```
mysql installieren:
```sh
sudo apt-get install mysql-server libmysql
```
mysqldb für flask installieren:
```sh
pip install flask-mysqldb
```
## Flask Hello World

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)
```

## Datenbank einrichten

```sql
CREATE DATABASE flaskapp;
USE flaskapp;
create table students(id INT(11) AUTO_INCREMENT PRIMARY KEY, vorname VARCHAR(100), nachname VARCHAR(100), matrikelnummer INT(11), studiengang VARCHAR(100), semester INT(11), email VARCHAR(100));
```

## Mysqldb einrichten

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)
```

## Port ändern

Standardmäßig hört Flask auf Port 5000.

```python
if __name__ == '__main__':
    app.run(debug=True, port=8080)
```

## Dummy Student erstellen

```sql
INSERT INTO students(vorname, nachname, matrikelnummer, studiengang, semester, email) VALUES ("Max", "Mustermann", 12345678, "Medieninformatik", 5, "max@mustermann.edu");
```

## Dummy Daten für Programmstart


## Routen

### /students
GET all students
```python
@app.route('/students')
def students():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM students''')
    rv = cur.fetchall()
    return str(rv)
```
POST a new Student

```python
@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        req = request.json
        vorname = req['first_name']
        nachname = req['last_name']
        matrikelnummer = req['matriculation_number']
        studiengang = req['course']
        email = req['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students(vorname, nachname, matrikelnummer, studiengang, email) VALUES (%s, %s, %s, %s, %s)", (vorname, nachname, matrikelnummer, studiengang, email))
        mysql.connection.commit()
        cur.close()
```

### /students/{id}
GET one student with specific id
```python
@app.route('/students/<string:id>/')
def student(id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM students WHERE id=''' + id)
    rv = cur.fetchall()
    return str(rv)
```

DELETE a student

```python
@app.route('/students/<string:id>', methods=['GET', 'DELETE'])
def student(id):
    cur = mysql.connection.cursor()
    if request.method == 'DELETE':
        cur.execute('''DELETE FROM students WHERE id=''' +id)
        mysql.connection.commit()
        cur.close()
        return "Student Deleted"
```

PATCH a student

```python
elif request.method == 'PATCH':
        req = request.json
        keys = req.keys()
        attribute = keys[0]
        val = "'" + req[attribute] + "'"
        cur.execute("UPDATE students SET " + attribute + "= " + val + " WHERE id="+ id)
        mysql.connection.commit()
        cur.close()
        return "Student updated"
```

## Logging

Kafka für Flask:

```python
pip install flask-kafka
```

Kafka einrichten:


```python
# kafka importieren
from kafka import SimpleProducer, KafkaClient

# Konfigurieren
kafka = KafkaClient('qq2.ddnss.de:9092')
producer = SimpleProducer(kafka)
topic = 'logging'

```


Nachricht senden, wenn eine Aktion ausgeführt wurde


```python
# GET auf /students
producer.send_messages(topic, '{\n"service_name": "1_Flask_1",\n "operation": "GET",\n "message": "Liste aller Studenten"\n}')

```

Message die gesendet werden soll:


```python
fabian@ThinkPad-X220:~/qq2/qq2$ python
Python 2.7.12 (default, Dec  4 2017, 14:50:18) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> print '{\n"service_name": "1_Flask_1",\n "operation": "GET",\n "message": "Liste aller Studenten"\n}'
{
"service_name": "1_Flask_1",
 "operation": "GET",
 "message": "Liste aller Studenten"
}

```

