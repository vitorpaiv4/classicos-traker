from flask import Flask, render_template
import sqlite3
import pandas as pd

app = Flask(__name__)

def get_car_data():
    conn = sqlite3.connect('carros.db')
    df = pd.read_sql_query("SELECT * FROM anuncios", conn)
    conn.close()
    return df.to_dict(orient='records') # Convert DataFrame to list of dictionaries

@app.route('/')
def index():
    car_data = get_car_data()
    return render_template('index.html', cars=car_data)

if __name__ == '__main__':
    app.run(debug=True)