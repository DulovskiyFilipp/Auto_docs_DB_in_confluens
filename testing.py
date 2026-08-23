import requests
import os
import time
from db import get_table_metadata
from jinja2 import Template

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


start_time = time.perf_counter()


pg_params = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '12345'
}

all_metadata = get_table_metadata(pg_params)


template = Template("""
<h2>Таблица: {{ table_name }}</h2>
<table>
<tr><th>Столбец</th><th>Тип</th><th>Nullable</th><th>Ограничение символов</th></tr>
{% for col in columns %}
<tr><td>{{ col[0] }}</td><td>{{ col[1] }}</td><td>{{ col[2] }}</td><td>{{ col[3] }}</td></tr>
{% endfor %}
</table>
""")


for key, val in all_metadata.items():
    html = template.render(table_name=key, columns=val)

    payload = {
        "spaceId": "131074",
        "status": "current",
        "title": f'Спецификация таблицы - {key}',
        "parentId": "11173889",
        "body": {
            "representation": "storage",
            "value": html
        }
    }

    resp = sessions.post(f'{BASE_URL}/api/v2/pages', json=payload)
    resp.raise_for_status()
    new_page = resp.json()
    #print(f"Создана страница с ID: {new_page['id']}")


end_time = time.perf_counter()
print(f"Время выполнения: {end_time - start_time:.6f} секунд")