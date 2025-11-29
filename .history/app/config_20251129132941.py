import os

class Config:
    SECRET_KEY = 'supersecretkey'

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://fashion_user:12345@localhost/fashionstock"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "super_secret_key")