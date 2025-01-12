from flask import request, jsonify
import sqlite3

from popularProduct import DATABASE


def add_product(app):
    @app.route('/add_product', methods=['POST'])
    def addProduct():
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO  products (name, description)
                VALUES (?, ?) 
            ''', (name, description))
            conn.commit()
            
            return jsonify({'message': 'products was added'})
        except Exception as e:
            return jsonify({'message something went wrong'})
        finally:
            cursor.close()

def get_product(app):
    @app.route('/products', methods=['GET'])
    def getting_product():
        conn = sqlite3.connect(DATABASE)        
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()

        res = [{'id': row['id'], 'name': row['name'], 'description': row['description']} for row in rows]

        conn.commit()
        conn.close()
        return jsonify(res)
    
def deleteProduct(app):
    @app.route('/delete_product', methods=['POST'])
    def delete_product():
        data = request.get_json()

        if not data or 'name' not in data:
            return jsonify({'message': 'Invalid input'}), 400

        name = data['name']

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM products WHERE name = ?', (name,))

            conn.commit()

            if cursor.rowcount == 0:
                return jsonify({'message': 'Product not found'}), 404

            return jsonify({'message': 'Product deleted successfully'})

        except Exception as err:
            return jsonify({'message': str(err)}), 500
        finally:
            conn.close()