from dotenv import load_dotenv
import os

load_dotenv()

POLYGON_URL = os.getenv("POLYGON_URL")
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")