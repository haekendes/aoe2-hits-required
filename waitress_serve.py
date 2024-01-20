import os
from waitress import serve
from application.app import app

serve(app, host='0.0.0.0',  port=os.getenv('PORT', default=5000))