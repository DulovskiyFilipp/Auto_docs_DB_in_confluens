from conf_connect import sessions, BASE_URL

def get_pages_schema(parent_page: int):
    """Запрос списка схем занесенных в confluence."""

    response = sessions.get(f"{BASE_URL}/api/v2/pages/{parent_page}/descendants", params={"body-format": "storage"})
    if response.status_code != 200:
        return False
    pages = response.json()
    list_page = []
    for page in pages['results']:
        list_page.append(page['title'])
    return list_page


def get_page_spec(page_name: str):
    """Запрос на проверку существования страницы спецификации."""

    response = sessions.get(f"{BASE_URL}/api/v2/pages", params={"title": page_name,
                                                                "body-format": "storage"})
    if response.status_code != 200:
        return False
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
    if response.status_code != 200:
        return False
    return True

def alter_page_spec(title: str, parent_id: int, page_template: str, page_id: int):
    """Запрос на обновление существующей страницы, или новые значения или метка удаления."""

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
    response = sessions.put(f"{BASE_URL}/api/v2/pages/{page_id}", json=payload)
    if response.status_code != 200:
        return False
    return True
