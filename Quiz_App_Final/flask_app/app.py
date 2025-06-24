from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
import random

app = Flask(__name__)

# PostgreSQL-Verbindung
def get_db_connection():
    return psycopg2.connect(
        host="db",
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
    cur.execute("SELECT quiz_name FROM quizzes")
    quizzes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("library.html", quizzes=[q[0] for q in quizzes])

@app.route('/myquizzes')
def myquizzes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT quiz_name FROM quizzes")
    quizzes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("myquizzes.html", quizzes=[q[0] for q in quizzes])

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        quiz_name = request.form['quiz_name']
        questions = request.form.getlist('question')
        answers = request.form.getlist('answer')
        answers2 = request.form.getlist('answer2')
        explanations = request.form.getlist('explanation')

        conn = get_db_connection()
        cur = conn.cursor()

        # Sicherstellen, dass die quizzes-Tabelle existiert
        cur.execute('''
            CREATE TABLE IF NOT EXISTS quizzes (
                id SERIAL PRIMARY KEY,
                quiz_name TEXT,
                table_name TEXT
            )
        ''')

        # Eindeutiger Tabellenname für das neue Quiz
        unique_table_name = f"quiz_{quiz_name.replace(' ', '_')}_{os.urandom(4).hex()}"

        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS "{unique_table_name}" (
                id SERIAL PRIMARY KEY,
                frage TEXT,
                antwort TEXT,
                antwort2 TEXT,
                beschreibung TEXT
            )
        ''')

        for q, a1, a2, e in zip(questions, answers, answers2, explanations):
            cur.execute(f'''
                INSERT INTO "{unique_table_name}" (frage, antwort, antwort2, beschreibung)
                VALUES (%s, %s, %s, %s)
            ''', (q, a1, a2, e))

        cur.execute('INSERT INTO quizzes (quiz_name, table_name) VALUES (%s, %s)', (quiz_name, unique_table_name))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('library'))

    return render_template("create_quiz.html")

@app.route('/quiz/<quizname>')
def play_quiz(quizname):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT table_name FROM quizzes WHERE quiz_name = %s', (quizname,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return "Quiz nicht gefunden!", 404

    table_name = row[0]
    cur.execute(f'SELECT frage, antwort, antwort2, beschreibung FROM "{table_name}"')
    rows = cur.fetchall()

    questions = []
    for r in rows:
        # Die richtige Antwort ist immer die erste (antwort)
        correct_answer = r[1]
        wrong_answer = r[2]

        # Zufällig entscheiden, ob A oder B die richtige Antwort ist
        if random.choice([True, False]):
            # A ist richtig
            options = [("A", correct_answer), ("B", wrong_answer)]
            correct_key = "A"
        else:
            # B ist richtig
            options = [("A", wrong_answer), ("B", correct_answer)]
            correct_key = "B"

        questions.append({
            "frage": r[0],
            "options": options,
            "correct": correct_key,
            "beschreibung": r[3]
        })

    cur.close()
    conn.close()

    return render_template("play_quiz.html", questions=questions, quizname=quizname)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
