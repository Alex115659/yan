from flask import jsonify, request
import os
import sqlite3

DATABASE = 'yan.db'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def popularProductAdding(app):
    @app.route('/add_popularProduct', methods=['POST'])
    def add_popular_product():
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if not (name and description):
            return jsonify({'error_message': 'Name and description are required'}), 400

        try:
            cursor.execute('''
            INSERT INTO popularProducts (name, description)
            VALUES (?, ?)
            ''', (name, description))
            conn.commit()
            print('Popular product added in database')
        except sqlite3.IntegrityError as e:
            return jsonify({'error_message': f'Database error: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'error_message': f'Unexpected error: {str(e)}'}), 500
        finally:
            cursor.close()
            conn.close()

        return jsonify({'message': 'Popular product added successfully'}), 201

def popularProductGetting(app):
    @app.route('/popular_product', methods=['GET'])
    def get_popular_product():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row  
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM popularProducts')
            rows = cursor.fetchall()
            arr = []
            for row in rows:
                arr.append({
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description']
                })
            return jsonify(arr), 200
        except Exception as e:
            return jsonify({
                'error': str(e), 
                'message': 'Something went wrong while fetching popular products.'
            }), 500
        finally:
            conn.close()  

def deletePopularProducts(app):
    @app.route('/delete_popularProduct', methods=['POST'])
    def delete_popularProducts():
        data = request.get_json()

        name = data.get('name')

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM popularProducts WHERE name = ?', (name, ))

            conn.commit()
            return jsonify({'message': 'all went okay'})
        except Exception as err:
            return jsonify({'message': err})
        finally:
            conn.close()