from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL-Verbindung
def get_db_connection():
    return psycopg2.connect(
        host="db",  # Container-Name aus Docker Compose
        database="mydb",
        user="myuser",
        password="mypassword"
    )

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/library')
def library():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema='public'
    """)
    quizzes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("library.html", quizzes=[q[0] for q in quizzes if not q[0].startswith("pg_")])

@app.route('/myquizzes')
def myquizzes():
    # (Später könnte man hier nur die eigenen Quizze anzeigen)
    return render_template("myquizzes.html")

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        quiz_name = request.form['quiz_name']
        questions = request.form.getlist('question')
        answers = request.form.getlist('answer')
        explanations = request.form.getlist('explanation')

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS "{quiz_name}" (
                id SERIAL PRIMARY KEY,
                frage TEXT,
                antwort TEXT,
                beschreibung TEXT
            )
        ''')

        for q, a, e in zip(questions, answers, explanations):
            cur.execute(f'''
                INSERT INTO "{quiz_name}" (frage, antwort, beschreibung)
                VALUES (%s, %s, %s)
            ''', (q, a, e))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('library'))
    
    return render_template("create_quiz.html")

@app.route('/quiz/<quizname>')
def play_quiz(quizname):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT frage, antwort, beschreibung FROM "{quizname}"')
    questions = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("play_quiz.html", questions=questions, quizname=quizname)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
