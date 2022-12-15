from flask import Flask, render_template
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = 'crud-flask-students'

DB_HOST = 'localhost'
DB_NAME = 'testdb'
DB_USER = 'postgres'
DB_PASS = 'guest@dmin'

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, passsword=DB_PASS, host=DB_HOST)


@app.route('/')

def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursors)
    s = "SELECT*FROM student"
    cur.execute(s) # Execute SQL
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
