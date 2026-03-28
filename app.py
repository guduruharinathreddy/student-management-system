from flask import Flask, render_template, request, redirect, session
import sqlite3   # ✅ ADD THIS

app = Flask(__name__)
app.secret_key = "secret123"

# Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple Admin Login
        if username == "admin" and password == "1234":
            session['user'] = username
            return redirect('/dashboard')
        else:
            return "Invalid Credentials ❌"
    
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        return redirect('/')
    import sqlite3

# Add Student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        marks = request.form['marks']
        attendance = request.form['attendance']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute("INSERT INTO students (name, age, course, marks, attendance) VALUES (?, ?, ?, ?, ?)",
                    (name, age, course, marks, attendance))

        conn.commit()
        conn.close()

        return redirect('/view')

    return render_template('add_student.html')


# View Students
@app.route('/view')
def view_students():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    data = cur.fetchall()

    conn.close()

    return render_template('view_students.html', students=data)
# Update Student
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        marks = request.form['marks']
        attendance = request.form['attendance']

        cur.execute("""
        UPDATE students
        SET name=?, age=?, course=?, marks=?, attendance=?
        WHERE id=?
        """, (name, age, course, marks, attendance, id))

        conn.commit()
        conn.close()

        return redirect('/view')

    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    conn.close()

    return render_template('update_student.html', student=student)
# Delete Student
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id=?", (id,))
    
    conn.commit()
    conn.close()

    return redirect('/view')
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
@app.route('/search', methods=['GET', 'POST'])
def search():
    students = []
    if request.method == 'POST':
        name = request.form['name']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + name + '%',))
        students = cur.fetchall()

        conn.close()

    return render_template('search.html', students=students)
import matplotlib.pyplot as plt

@app.route('/graph')
def graph():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT name, marks FROM students")
    data = cur.fetchall()

    conn.close()

    if not data:
        return "No data available to plot ❌"

    names = [i[0] for i in data]
    marks = [i[1] for i in data]

    plt.figure()
    plt.bar(names, marks)
    plt.xlabel("Students")
    plt.ylabel("Marks")
    plt.title("Student Marks Analysis")

    plt.savefig('static/graph.png')  # save inside static
    plt.close()

    return render_template('graph.html')
if __name__ == '__main__':
    app.run(debug=True)