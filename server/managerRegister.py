from flask import jsonify, request
import sqlite3

DATABASE = 'yan.db'

def addManager(name, email, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute('''
        INSERT INTO manager (name, email, password)
        VALUES (?, ?, ?)
        ''', (name, email, password))
        conn.commit()  
        print(f"Manager {name} added successfully")
    except sqlite3.IntegrityError as e:  
        print(f"Error adding manager: {e}")
    finally:
        conn.close() 


def manager_getting(app):
    @app.route('/manager', methods=['GET'])
    def manager():
        try:
            conn = sqlite3.connect(DATABASE)
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM manager')
            rows = cursor.fetchall()

            managers = []
            for row in rows:
                managers.append({
                    'id': row['id'],  
                    'name': row['name'],
                    'email': row['email'],
                    'password': row['password']
                })

            return jsonify(managers), 200
        except sqlite3.Error as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            conn.close()
