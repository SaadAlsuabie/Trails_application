from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    def __init__(self):
        self.dbdriver = os.getenv('DB_DRIVER')
        self.dbname = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.auth_url = os.getenv('AUTH_URL')
