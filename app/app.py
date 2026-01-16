
# app/app.py
from flask import Flask, request, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

# Flag: skip DB in CI/demo mode when SKIP_DB=1
SKIP_DB = os.environ.get('SKIP_DB') == '1'

db_config = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', 'root'),
    'database': os.environ.get('DB_NAME', 'usersdb')
}

def init_db_if_needed():
    """Create table only when DB is enabled."""
    if SKIP_DB:
        return
    # In real envs you might want to wait for DB
    time.sleep(10)
    conn = mysql.connector.connect(**db_config)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        ''')
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Initialize DB only if not skipping
init_db_if_needed()


@app.route('/', methods=['GET'])
def addusers_form():
    return """
        <!doctype html>
        <html>
          <head><title>Add User</title></head>
          <body>
            <h2>Add User</h2>
            /submituser
              <label>Name: <input type="text" name="name" required></label><br><br>
              <label>Email: <input type="email" name="email" required></label><br><br>
              <input type="submit" value="Add User">
            </form>
            <p>/usersView all users (JSON)</a></p>
          </body>
        </html>
    """

@app.route('/submituser', methods=['POST'])
def submit_user():
    name = (request.form.get('name') or '').strip()
    email = (request.form.get('email') or '').strip()

    if not name or not email:
        return (
            """
            <p>Name and Email are required.</p>
            <p>/Go back</a></p>
            """,
            400,
        )

    if SKIP_DB:
        # Demo/CI mode: do not hit DB
        return f"""
            <p>Demo mode: User <strong>{name}</strong> would be added!</p>
            <p>/Add another</a></p>
        """

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        app.logger.error(f"Insert failed: {e}")
        return (
            f"""
            <p>Failed to add user due to a database error.</p>
            <pre>{e}</pre>
            <p>/Go back</a></p>
            """,
            500,
        )

    return f"""
        <p>User <strong>{name}</strong> added successfully!</p>
        <p>/Add another</a></p>
        <p>/usersView users</a></p>
    """

@app.route('/users', methods=['GET'])
def get_users():
    if SKIP_DB:
        # Demo/CI mode: return empty list
        return jsonify([])

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email FROM users')
        users = [{"id": row[0], "name": row[1], "email": row[2]} for row in cursor.fetchall()]
        cursor.close()
        conn.close()
    except Error as e:
        app.logger.error(f"Select failed: {e}")
        return jsonify({"error": "Database error", "details": str(e)}), 500

    return jsonify(users)

if __name__ == '__main__':
    # Only for local dev runs; in production use a WSGI server (gunicorn/uwsgi)
    app.run(host='0.0.0.0', port=5000)



