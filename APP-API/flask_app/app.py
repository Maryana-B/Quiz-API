from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def get_quiz_data():
    conn = psycopg2.connect(
        host="db",  # Container-Name aus Docker Compose als Host
        database="mydb",
        user="myuser",
        password="mypassword"
    )
    cur = conn.cursor()
    cur.execute("SELECT frage, antwort, beschreibung FROM quiz")
    daten = cur.fetchall()
    cur.close()
    conn.close()
    return daten

@app.route('/')
def index():
    quiz_daten = get_quiz_data()
    return render_template('index.html', quiz=quiz_daten)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
