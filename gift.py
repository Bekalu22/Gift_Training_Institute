from flask import Flask, render_template, request

import sqlite3 as sql
"""
conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE students (name TEXT, gender TEXT, age int, email TEXT, subject TEXT,sdate datetime, emessage TEXT)')
print ("Table created successfully")
conn.close()
"""

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/enternew')
def new_student():
    return render_template('student.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            name = request.form['name']
            gender = request.form['gender']
            age = request.form['age']
            email = request.form['email']
            subject = request.form['subject']
            sdate = request.form['sdate']
            emessage = request.form['message']

            with sql.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO students (name,gender,age,email,subject,sdate,emessage)VALUES(?, ?, ?, ?, ?, ?, ?)",(name,gender,age,email,subject,sdate,emessage) )

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)