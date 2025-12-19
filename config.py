import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'attendance_system')
    
    # Path Configuration
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    IMAGES_DIR = os.path.join(DATA_DIR, 'images')
    TEMP_DIR = os.path.join(DATA_DIR, 'temp')
    
    # Face Recognition Configuration
    FACE_CASCADE_PATH = os.path.join(ASSETS_DIR, 'haarcascade_frontalface_default.xml')
    CAPTURE_DELAY = 3  # seconds
    
    # UI Configuration
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 600
    BG_COLOR = 'grey'
    
    @staticmethod
    def get_db_config():
        """Return database configuration as dictionary"""
        return {
            'host': Config.DB_HOST,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD,
            'database': Config.DB_NAME
        }
    
    @staticmethod
    def ensure_directories():
        """Ensure all required directories exist"""
        directories = [
            Config.ASSETS_DIR,
            Config.DATA_DIR,
            Config.IMAGES_DIR,
            Config.TEMP_DIR
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
