from flask import Flask, jsonify, request
from flask_cors import CORS
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
import mysql.connector

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host= DB_HOST,
        user= DB_USER,
        password= DB_PASSWORD,
        database= DB_NAME,
        port= DB_PORT
    )

@app.route('/trips', methods=['GET'])
def get_trips():
    continent = request.args.get('continent')  # filtro opzionale
    month = request.args.get('month')  # filtro opzionale
    place = request.args.get('place')  # filtro opzionale

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if continent:
        query = f"SELECT t.price, t.month, t.start_date, t.end_date, t.age, t.link, t.nights, d.name AS destination_name, d.country AS country_name, c.name AS continent_name, b.name AS brand_name FROM trips t JOIN destinations d ON t.destination_id = d.id JOIN continents c ON d.continent_id = c.id JOIN brand b ON d.brand_id = b.id WHERE t.month = '{month}' AND c.name = '{continent}';";
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(results)
    elif place:
        if place.lower() == 'ovunque':
            query = f"SELECT t.price, t.month, t.start_date, t.end_date, t.age, t.link, t.nights, t.flight, t.image_trip, t.year, d.name AS destination_name, d.country AS country_name, c.name AS continent_name, b.name AS brand_name FROM trips t JOIN destinations d ON t.destination_id = d.id JOIN continents c ON d.continent_id = c.id JOIN brand b ON d.brand_id = b.id WHERE t.month = '{month}';";
        else:
            query = f"SELECT t.price, t.month, t.start_date, t.end_date, t.age, t.link, t.nights, t.flight, t.image_trip, t.year, d.name AS destination_name, d.country AS country_name, c.name AS continent_name, b.name AS brand_name FROM trips t JOIN destinations d ON t.destination_id = d.id JOIN continents c ON d.continent_id = c.id JOIN brand b ON d.brand_id = b.id WHERE t.month = '{month}' AND d.name LIKE '%{place}%';";
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(results)
    else:
        return('API')

if __name__ == '__main__':
    app.run(debug=True)
