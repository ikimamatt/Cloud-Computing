import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS  # Import Flask-CORS

# Fungsi untuk koneksi ke database PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            database=os.environ.get("DB_NAME", "db_test"),
            user=os.environ.get("DB_USER", "mamat"),
            password=os.environ.get("DB_PASSWORD", "123")
        )
        print("Database connected successfully")  # Log database connection
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        raise e

# Inisialisasi Flask
app = Flask(__name__)

# Izinkan CORS hanya untuk route tertentu
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/')
def home():
    return jsonify({"message": "Hello from Flask!"})

# Endpoint untuk membaca data dari tabel 'items'
@app.route('/api/items', methods=['GET'])
def get_items():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, description FROM items;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        items = [{"id": row[0], "name": row[1], "description": row[2]} for row in rows]
        return jsonify(items)
    except Exception as e:
        print("Error fetching data:", e)  # Log error when fetching data
        return jsonify({"error": "Internal Server Error"}), 500

# Endpoint untuk menambahkan data ke tabel 'items'
@app.route('/api/items', methods=['POST'])
def create_item():
    try:
        data = request.json
        name = data['name']
        description = data['description']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id;", (name, description))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"id": new_id, "name": name, "description": description}), 201
    except Exception as e:
        print("Error inserting data:", e)  # Log error when inserting data
        return jsonify({"error": "Internal Server Error"}), 500

# Jalankan Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
