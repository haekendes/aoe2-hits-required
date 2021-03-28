import os

from flask import render_template, send_from_directory
from application.app import app, table_data, column_names


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/get_table', methods=['GET'])
def get_table():
    return {"table": table_data, "columns": column_names}

