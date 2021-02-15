import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode
from config_keys import user_token


def get_token():
    APP_ID = 7637207
    OAUTH_URL = "https://oauth.vk.com/authorize"
    REDIRECT_URI = "https://oauth.vk.com/blank.html"
    SCOPE = "status"
    OAUTH_PARAMS = {
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "response_type": "token",
        "client_id": APP_ID
    }
    print('?'.join([OAUTH_URL, urlencode(OAUTH_PARAMS)]))
    return True


def info_celtics_wiki():
    content = f"https://ru.wikipedia.org/wiki/" \
              f"%D0%91%D0%BE%D1%81%D1%82%D0%BE%D0%BD_%D0%A1%D0%B5%D0%BB%D1%82%D0%B8%D0%BA%D1%81"
    response = f"Ссылка на статью про Boston_Celtics с Википедии:\n{content}"

    return response


def news_celtics():
    response = requests.get("https://www.sports.ru/boston-celtics/")
    parser = BeautifulSoup(response.text, "html.parser")
    res = parser.find_all("div", class_="nl-item")
    some_list = []
    for i in res:
        article = i.find_all("a", class_="short-text")
        for news in article:
            link = news["href"]
            for name in news:
                description = name
                some_list.append(f"Название: {description} -> Ссылка: {link}")
    return some_list


def parse_bot_user(vk_id):
    V = "5.126"
    API_BASE_URL = "https://api.vk.com/method/"
    link = urljoin(API_BASE_URL, "users.get")
    response = requests.get(link,
                            params={
                                "access_token": user_token,
                                "v": V,
                                "user_ids": vk_id,
                                "fields": ["sex, status"]
                            })
    response_json = response.json()["response"]
    some_dict = {}
    for i in response_json:
        some_dict["name"] = i["first_name"]
        some_dict["surname"] = i["last_name"]
        some_dict["ID"] = i["id"]
        some_dict["gender"] = i["sex"]
    return some_dict


def get_photos(owner_user_id):
    API_BASE_URL = "https://api.vk.com/method/"
    API_BASE_VERSION = "5.77"
    link = urljoin(API_BASE_URL, "photos.get")
    res = requests.get(
        link,
        params={
            "access_token": user_token,
            "v": API_BASE_VERSION,
            "album_id": "profile",
            "extended": 1,
            "owner_id": owner_user_id,
            "photo_sizes": 1,
            "count": 1000
        },
    )
    res_json = res.json()["response"]["items"]
    likes_nums = sorted(list({like_photo["likes"]["count"] for like_photo in res_json}))
    likes_list = likes_nums[-3:]
    som = []
    for photo in res_json:
        if photo["likes"]["count"] in likes_list:
            some_dict = {"ID": photo["id"], "likes": photo["likes"]["count"]}
            som.append(some_dict)
    return som


def search_country_for_db():
    V = "5.126"
    API_BASE_URL = "https://api.vk.com/method/"
    link = urljoin(API_BASE_URL, "database.getCountries")
    response = requests.get(link,
                            params={
                                "access_token": user_token,
                                "v": V,
                                "need_all": 1,
                                "count": 1000
                            })
    response_json = response.json()["response"]["items"]
    return response_json


def search_city_for_db(c_id):
    V = "5.126"
    API_BASE_URL = "https://api.vk.com/method/"
    link = urljoin(API_BASE_URL, "database.getCities")
    response = requests.get(link,
                            params={
                                "access_token": user_token,
                                "v": V,
                                "country_id": c_id,
                                "need_all": 0,
                                "count": 1000
                            })
    response_json = response.json()["response"]["items"]
    return response_json


def search_users(age_from, age_to, gender, town, status, country):
    V = "5.126"
    API_BASE_URL = "https://api.vk.com/method/"
    link = urljoin(API_BASE_URL, "users.search")
    response = requests.get(link,
                            params={
                                "sort": 0,
                                "access_token": user_token,
                                "age_from": age_from,
                                "age_to": age_to,
                                "sex": gender,
                                "status": status,
                                "v": V,
                                "country": country,
                                "fields": ["sex, country, city, is_closed, can_access_closed"],
                                "count": 1000,
                                "has_photo": 1
                            })
    response_json = response.json()["response"]["items"]
    users = ({"name": i["first_name"], "surname": i["last_name"], "User_ID": i["id"],
              "city": i["city"], "country": i["country"], "gender": i["sex"], "is_closed": i["is_closed"]}
             for i in response_json if "city" in i and town.lower() in i["city"]["title"].lower() and "country" in i
             and 'is_closed' in i and i['is_closed'] is False)
    return users


