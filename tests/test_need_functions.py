import pytest

from need_functions_modules import get_token, info_celtics_wiki, news_celtics, parse_bot_user, get_photos, \
    search_country_for_db, search_city_for_db, search_users


class Testneedfunctions:

    def setup_class(self):
        print("setup method")

    def test_method_get_token(self):
        assert get_token() == True

    def test_method_celtics_info_wiki(self):
        assert "https://ru.wikipedia.org/wiki/" in info_celtics_wiki()

    def test_method_news_celtics(self):
        assert ("Название" and "Ссылка") in str(news_celtics())

    def test_parse_bot_user(self):
        assert ("name" and "surname" and "ID" and "gender") in parse_bot_user(69332752).keys()

    def test_get_photos(self):
        assert ("ID" and "likes") in get_photos(69332752)[0]

    def test_search_country_for_db(self):
        assert ("id" and "title") in search_country_for_db()[0]

    def test_search_city_for_db(self):
        assert ("id" and "title") in search_city_for_db(1)[0]

    def test_search_users(self):
        test = search_users(18, 20, 1, "москва", 1, 1)
        for i in test:
            assert "москва" in i['city']['title'].lower()

    def teardown_class(self):
        print("method teardown")


