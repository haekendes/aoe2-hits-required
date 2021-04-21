from flask import Flask
from flask_bootstrap import Bootstrap
from application.aoe.prepare_data import get_column_names, get_table_data
from config import Config

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)

column_names = get_column_names()
table_data = get_table_data()

from application import routes
