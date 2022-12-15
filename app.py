from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = 'crud-flask-students'

DB_HOST = 'localhost'
DB_NAME = 'testdb'
DB_USER = 'postgres'
DB_PASS = 'guest@dmin'

conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)


@app.route('/')

def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT*FROM students"
    cur.execute(s) # Execute SQL
    list_user = cur.fetchall()
    return render_template('index.html', list_user=list_user)

@app.route('/add_student', methods={"POST"})

def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        cur.execute("INSERT INTO students (fname, lname, email) VALUES (%s,%s,%s)", (fname, lname, email))
        conn.commit()
        flash ('User added successfuly')
        return redirect(url_for('Index'))



if __name__ == '__main__':
    app.run(debug=True)
