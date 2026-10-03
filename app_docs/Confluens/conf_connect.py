import os
import requests

from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("CONFLUENCE_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
BASE_URL = os.getenv("CONFLUENCE_BASE_URL")

sessions = requests.Session()
sessions.auth = (EMAIL, API_TOKEN)
sessions.headers.update({
    "Accept": "application/json",
    "Content-Type": "application/json"
})

