from flask import Flask

# Flask Plugins
from config import Config

app = Flask(__name__)
# Load Config
app.config.from_object(Config)


from app import routes