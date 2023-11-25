from dotenv import load_dotenv
import os
load_dotenv('.env')


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
