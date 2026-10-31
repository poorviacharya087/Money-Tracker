from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("money.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_database():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            transaction_type TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = get_db()
    transactions = conn.execute(
        "SELECT * FROM transactions ORDER BY id DESC"
    ).fetchall()

    income = conn.execute(
        "SELECT SUM(amount) FROM transactions WHERE transaction_type='Income'"
    ).fetchone()[0] or 0

    expenses = conn.execute(
        "SELECT SUM(amount) FROM transactions WHERE transaction_type='Expense'"
    ).fetchone()[0] or 0

    conn.close()

    balance = income - expenses

    return render_template(
        "index.html",
        transactions=transactions,
        income=income,
        expenses=expenses,
        balance=balance
    )

@app.route("/add", methods=["POST"])
def add_transaction():
    title = request.form["title"]
    amount = float(request.form["amount"])
    category = request.form["category"]
    transaction_type = request.form["transaction_type"]

    conn = get_db()
    conn.execute(
        "INSERT INTO transactions (title, amount, category, transaction_type) VALUES (?, ?, ?, ?)",
        (title, amount, category, transaction_type)
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    conn = get_db()
    conn.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    create_database()
    app.run(debug=True)