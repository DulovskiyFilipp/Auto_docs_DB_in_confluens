import os
import requests

from dotenv import load_dotenv
load_dotenv()

EMAIL = os.getenv("CONFLUENCE_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
BASE_URL = os.getenv("CONFLUENCE_BASE_URL")


#Запрос списка схем занесенных в confluence
def get_schema_page():
    pass


#Запрос на создание страницы схемы
def create_page_schema():
    pass


#Запрос на создание старницы спецификации
def create_page_spec():
    pass


#Запрос на обновление существующей страницы
def update_page_spec():
    pass


#Запрос на обновление страницы при удалении объекта
def alter_page_del():
    pass





