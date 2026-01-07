from flask import Flask, request, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

# Wait for MySQL to be ready
time.sleep(10)

db_config = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', 'root'),
    'database': os.environ.get('DB_NAME', 'usersdb')
}

# Create table if not exists
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
    )
''')
conn.commit()
cursor.close()
conn.close()

@app.route('/', methods=['GET'])
def addusers_form():
    return '''
        &lt;h2&gt;Add User&lt;/h2&gt;
        &lt;form method="post" action="/submituser"&gt;
            Name: &lt;input type="text" name="name"&gt;&lt;br&gt;&lt;br&gt;
            Email: &lt;input type="email" name="email"&gt;&lt;br&gt;&lt;br&gt;
            &lt;input type="submit" value="Add User"&gt;
        &lt;/form&gt;
    '''
OBOBOBOBOB
@app.route('/submituser', methods=['POST'])
OBdef submit_user():
OBOB    name = request.form['name']
    email = request.form['email']
OB    conn = mysql.connector.connect(**db_config)
OB    cursor = conn.cursor()
OB    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
OBOB    conn.commit()
    cursor.close()
OB    conn.close()
OB    return f'&lt;p&gt;User {name} added successfully!&lt;/p&gt;&lt;a href="/"&gt;Add another&lt;/a&gt;'
OB
@app.route('/users', methods=['GET'])
def get_users():
OB    conn = mysql.connector.connect(**db_config)
OB    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email FROM users')
OBOBOBOB    users = [{"id": row[0], "name": row[1], "email": row[2]} for row in cursor.fetchall()]
OB    cursor.close()
    conn.close()
OB    return jsonify(users)
OB
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
