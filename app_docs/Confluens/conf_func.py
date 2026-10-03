from conf_connect import sessions, BASE_URL

parent_page = 12943372
def get_schema_page():
    """Запрос списка схем занесенных в confluence."""
    response = sessions.get(f"{BASE_URL}/api/v2/pages/{parent_page}/descendants", params={"body-format": "storage"})
    response.raise_for_status()
    pages = response.json()
    list_page = []
    for page in pages['results']:
        list_page.append(page['title'])
    return list_page


def get_page_spec(page_name: str):
    """Запрос на проверку существования страницы спецификации."""
    response = sessions.get(f"{BASE_URL}/api/v2/pages", params={"title": page_name,
                                                                    "body-format": "storage"})
    response.raise_for_status()
    page = response.json()
    if len(page['results']) > 0:
        return True
    else:
        return False


def create_page(parent_id: int, title: str, page_template: str):
    """Запрос на создание страницы схемы или спецификации."""
    payload = {
        "spaceId": "131074",
        "status": "current",
        "title": title,
        "parentId": parent_id,
        "body": {
            "representation": "storage",
            "value": page_template
        }
    }
    response = sessions.post(f"{BASE_URL}/api/v2/pages", json=payload)
    response.raise_for_status()


def update_page_spec():
    """Запрос на обновление существующей страницы."""
    pass


def alter_page_del():
    """Запрос на обновление страницы при удалении объекта."""
    pass

#get_schema_page()
#get_page_spec('Спецификации таблиц в БД - Service_note')