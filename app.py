from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = 'crud-flask-students'

DB_HOST = 'dpg-cehjldmn6mpg3l7rbtgg-a'
DB_NAME = 'testdb_render'
DB_USER = 'testdb_render_user'
DB_PASS = 'RPcYGNAj2Xeb9CkPJIXUpEmNtvT7GPQQ'

conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)


@app.route('/')

def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT*FROM students"
    cur.execute(s) # Execute SQL
    list_user = cur.fetchall()
    return render_template('index.html', list_user=list_user)

@app.route('/add_student', methods=["POST"])

def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        cur.execute("INSERT INTO students (fname, lname, email) VALUES (%s,%s,%s)", (fname, lname, email))
        conn.commit()
        flash ('User Added Successfuly')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods=['GET', 'POST'])

def get_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT*FROM students WHERE id = %s", (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', student = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""UPDATE students
                        SET fname = %s,
                              lname = %s,
                              email = %s
                        WHERE id = %s
        """, (fname, lname, email, id))
        conn.commit()
        flash ('User Updated Successfuly')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods=['POST','GET'])
def delete_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM students WHERE id = {0}'.format(id))
    conn.commit()
    flash ('User Deleted Successfuly')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(debug=True)
