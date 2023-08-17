from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

URL: str = os.getenv("URL")
LOGIN: str = os.getenv("LOGIN")
PASSWORD: str = os.getenv("PASSWORD")

TABLE_NAME: str = os.getenv("TABLE_NAME")
STRING_CONNECTION: str = os.getenv("STRING_CONNECTION")

FILE_PATH: str = os.getenv("FILE_PATH")