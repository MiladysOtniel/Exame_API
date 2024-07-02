from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# banco de dados
def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                logged_in INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

# Registrar um novo usuário
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            return jsonify({'message': 'Usuário registrado com sucesso!'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'E-mail já registrado!'}), 400

# Fazer login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'E-mail e senha são obrigatórios!'}), 400

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if user:
            stored_password = user[3]  # índice 3 corresponde à coluna 'password'
            if password == stored_password:
                if user[4] == 1:
                    return jsonify({'error': 'Usuário já está logado em outro dispositivo!'}), 401
                else:
                    cursor.execute('UPDATE users SET logged_in = 1 WHERE email = ?', (email,))
                    conn.commit()
                    return jsonify({'message': 'Login realizado com sucesso!'}), 200
            else:
                return jsonify({'error': 'Senha incorreta!'}), 401
        else:
            return jsonify({'error': 'Usuario não encontrado!'}), 401

# Fazer logout
@app.route('/api/logout/<int:user_id>', methods=['GET'])
def logout(user_id):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET logged_in = 0 WHERE id = ?', (user_id,))
        conn.commit()
        return jsonify({'message': 'Logout realizado com sucesso!'}), 200

# Rota para obter todos os usuários (admin)
@app.route('/api/users', methods=['GET'])
def get_users():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email FROM users')
        users = [{'id': row[0], 'username': row[1], 'email': row[2]} for row in cursor.fetchall()]
        return jsonify(users)

if __name__ == '__main__':
    init_db()  
    app.run(debug=True)
