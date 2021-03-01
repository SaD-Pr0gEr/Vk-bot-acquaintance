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
        news = news_celtics()
        assert all(i in str(news) for i in ("Название:", "Ссылка:"))

    def test_parse_bot_user(self):
        user = parse_bot_user(616586034)
        assert all(i in user for i in ("name", "surname", "ID", "gender"))

    def test_get_photos(self):
        photos = get_photos(616586034)
        assert all(i in str(photos) for i in ("ID", "likes"))

    def test_search_country_for_db(self):
        countrys = search_country_for_db()
        assert all(i in countrys[0] for i in ["id", "title"])

    def test_search_city_for_db(self):
        cities = search_city_for_db(1)
        assert all(i in cities[0] for i in ["id", "title"])

    def test_search_users(self):
        test = search_users(18, 20, 1, "москва", 1, 1)
        for i in test:
            assert all(a in i for a in ("name", "surname", 'User_ID'))

    def teardown_class(self):
        print("method teardown")


