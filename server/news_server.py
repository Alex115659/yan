from flask import jsonify, request
import sqlite3

DATABASE = 'yan.db'

def add_news(app):
    @app.route('/add_news', methods=['POST'])
    def addNews():
        data = request.get_json()
        description = data.get('description')
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute('''
            INSERT INTO news (description)
            VALUES (?)
            ''', (description,))
            conn.commit()

            news_id = cursor.lastrowid
            return jsonify({'message': 'News was added successfully', 'id': news_id})
        except Exception as e:
            return jsonify({'message': 'Something went wrong', 'error': str(e)}), 500
        finally:
            conn.close()


def get_news(app):
    @app.route('/get_news', methods=['GET'])
    def gettingNews():
        try:
            conn = sqlite3.connect(DATABASE)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM news')
            rows = cursor.fetchall()

            res = [{'id': row['id'], 'description': row['description']} for row in rows]

            conn.commit()
            return jsonify(res)

        except Exception as e:
            return jsonify({'message': 'Something went wrong', 'error': str(e)}), 500
        finally:
            conn.close()

def deleteNews(app):
    @app.route('/delete_news', methods=['POST'])
    def delete_news():
        data = request.get_json()

        name = data.get('name')

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM news WHERE description = ?', (name,))

            conn.commit()
            return jsonify({'message': 'all went okay'})

        except Exception as err:
            return jsonify({'message': err})
        finally:
            conn.close()

