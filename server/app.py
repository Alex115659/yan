import os
import logging
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from popularProduct import popularProductAdding, popularProductGetting, deletePopularProducts
from managerRegister import addManager, manager_getting
from news_server import add_news, get_news, deleteNews
from products import add_product, get_product, deleteProduct

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'yan.db')
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS popularProducts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def addTable():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS manager (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating manager table: {e}")
    finally:
        conn.close()

def add_column():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
            ALTER TABLE clientsData
            ADD COLUMN surname TEXT
        ''')
    conn.commit()
    conn.close()

def add_Table3():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('PRAGMA journal_mode=WAL;')
    cursor.execute('DROP TABLE client')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientsDATA (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        product TEXT NOT NULL,
        description TEXT NOT NULL,
        price INTEGER NOT NULL,
        email TEXT NOT NULL,
        phoneNumber INTEGER NOT NULL      
    )
    ''')
    conn.commit()
    conn.close()

def add_Table2():
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL
            )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating manager table: {e}")
        finally:
            conn.close()


@app.route('/add_client', methods=['POST'])
def add_client():
    data = request.get_json()
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientsDATA (name, surname, price, description, product, email, phoneNumber)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['surname'], data['price'], data['description'], data['product'], data['email'], data['phoneNumber']))
        conn.commit()
        return jsonify({'message': 'Client added successfully'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/clients', methods=['GET'])
def clients():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM clientsDATA')
        rows = cursor.fetchall()

        res = []
        for row in rows:
            res.append({
                'id': row['id'],
                'name': row['name'],
                'surname': row['surname'],
                'email': row['email'],
                'product': row['product'],
                'phoneNumber': row['phoneNumber'],
                'price': row['price'],
                'description': row['description'],
            })
        return jsonify(res)
    except Exception as e:
        return jsonify({'error': e})
    
@app.route('/deleteClient', methods=['POST'])
def deleteClient():
    data = request.get_json()
    client_id = data.get('id')

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM clientsDATA WHERE id = ?', (client_id,))
        conn.commit()

        return jsonify({'result': 'done'})
    except Exception as err:
        return jsonify({'message': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/getManager', methods=['POST'])
def getManager():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM manager WHERE name = ? AND password = ? AND email = ?', (name, password, email))
        manager = cursor.fetchone() 

        if manager:
            return jsonify({
                'message': 'Manager was registered',
                'manager': {
                    'id': manager['id'],
                    'name': manager['name'],
                    'email': manager['email']
                }
            }), 200
        else:
            return jsonify({'message': 'No manager found'}), 404
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Something went wrong'}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    init_db() 
    popularProductAdding(app)  
    popularProductGetting(app) 
    add_news(app)
    get_news(app)
    manager_getting(app)
    add_product(app) 
    get_product(app)
    deleteProduct(app)
    deletePopularProducts(app)
    deleteNews(app)
    addManager('Aleks', 'windows02@internet.ru', 'alexik020911')  
    app.run(debug=True)