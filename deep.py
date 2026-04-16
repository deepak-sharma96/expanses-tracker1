from flask import Flask, request, jsonify, render_template_string
import sqlite3
import deep.html


app = Flask(__name__)

# ----------- DATABASE -----------
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()



# ----------- ROUTES -----------
@app.route('/')
def home():
    return render_template_string(HOME_HTML)

@app.route('/get_expenses')
def get_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    data = [{"id": r[0], "name": r[1], "amount": r[2]} for r in c.fetchall()]
    conn.close()
    return jsonify(data)

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (name, amount) VALUES (?, ?)", (data['name'], data['amount']))
    conn.commit()
    conn.close()
    return '', 204

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return '', 204

@app.route('/expenses')
def expenses_page():
    return render_template_string(EXPENSES_HTML)

# ----------- RUN -----------
if __name__ == "__main__":
    print("Server starting on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
