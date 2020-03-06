from flask import Flask

# Flask Plugins
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)
# Load Config
app.config.from_object(Config)

# Initialize Plugins
bootstrap = Bootstrap(app)

from app import routes