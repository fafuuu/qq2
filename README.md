# QQ2 Dokumenation
Hier ist die Vorgehensweise der Bearbeitung des QQ2 Projektes dokumentiert.
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



