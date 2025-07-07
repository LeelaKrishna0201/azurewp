from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL connection config
DB_HOST = os.environ.get("DB_HOST", "your-db.postgres.database.azure.com")
DB_NAME = os.environ.get("DB_NAME", "feedbackdb")
DB_USER = os.environ.get("DB_USER", "your_user@your-db")
DB_PASS = os.environ.get("DB_PASS", "your_password")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        sslmode="require"
    )

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        comment = request.form["comment"]

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO feedback (name, comment) VALUES (%s, %s)", (name, comment))
                conn.commit()

        return redirect("/")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name, comment, created_at FROM feedback ORDER BY id DESC")
            rows = cur.fetchall()

    return render_template("index.html", feedback=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
