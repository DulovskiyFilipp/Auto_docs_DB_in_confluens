import requests
import os
import time

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

# # ----------------- Запрос всех пространств
# resp = sessions.get(f"{BASE_URL}/api/v2/spaces", params={"limit": 25})
# resp.raise_for_status()
# data = resp.json()
#
# for space in data["results"]:
#     print(space["id"], space["key"], space["name"])


# #----------------- Парсинг сраницы по номеру
# page_id = '2916353'
# resp = sessions.get(f"{BASE_URL}/api/v2/pages/{page_id}", params={"body-format": "storage"})
#
# resp.raise_for_status()
# page = resp.json()
#
# print(page["title"])
# print(page["body"]["storage"]["value"])



# #------------------------------Создание новой страницы
# start_time = time.perf_counter()

# payload = {
#     "spaceId": "131074",
#     "status": "current",
#     "title": "Моя вторая страница из python",
#     "parentId": "10092550",
#     "body": {
#         "representation": "storage",
#         "value": f'<p> Привет моя страница номер 2</p>'
#     }
# }

# resp = sessions.post(f'{BASE_URL}/api/v2/pages', json=payload)
# resp.raise_for_status()
# new_page = resp.json()
# print(f"Создана страница с ID: {new_page['id']}")
#
# end_time = time.perf_counter()
# print(f"Время выполнения: {end_time - start_time:.6f} секунд")


#---------------------------------- Удаление созданных страниц
start_time = time.perf_counter()
def get_direct_children(page_id: str) -> list[dict]:
    """Возвращает ВСЕХ прямых потомков страницы, проходя по всем страницам пагинации."""
    children = []
    url = f"{BASE_URL}/api/v2/pages/{page_id}/children"
    params = {"limit": 250}  # максимум за один запрос

    while url:
        resp = sessions.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        #print(data)
        children.extend(data["results"])

        next_link = data.get("_links", {}).get("next")
        if next_link:
            # next_link уже содержит путь вида /wiki/api/v2/pages/...
            url = f"{BASE_URL.rsplit('/wiki', 1)[0]}{next_link}"
            params = None  # параметры уже включены в next_link
        else:
            url = None
    #print(children)
    return children


def delete_page_with_children(page_id: str, purge: bool = False):
    # 1. Находим ВСЕХ дочерних страниц (с учётом пагинации)
    children = get_direct_children(page_id)

    # 2. Рекурсивно удаляем детей сначала (снизу вверх по дереву)
    for child in children:
        sessions.delete(f"{BASE_URL}/api/v2/pages/{child['id']}")


delete_page_with_children("11173889", purge=False)
end_time = time.perf_counter()
print(f"Время выполнения: {end_time - start_time:.6f} секунд")
