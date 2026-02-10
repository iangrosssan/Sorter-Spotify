import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.join(basedir, '..')
load_dotenv(os.path.join(parent_dir, '.env'))

class Config:
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:8888/callback")
    
    @staticmethod
    def validate():
        if not Config.SPOTIPY_CLIENT_ID or not Config.SPOTIPY_CLIENT_SECRET:
            raise ValueError("Environment variables SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET must be set.")
