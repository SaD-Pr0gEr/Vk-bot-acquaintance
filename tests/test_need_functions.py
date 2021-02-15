import pytest

from need_functions_modules import get_token, info_celtics_wiki, news_celtics, parse_bot_user, get_photos, \
    search_country_for_db, search_city_for_db, search_users


class Testneedfunctions:

    def setup_class(self):
        print("setup method")

    def test_method_get_token(self):
        assert get_token() == True

    def test_method_celtics_info_wiki(self):
        assert info_celtics_wiki()

    def test_method_news_celtics(self):
        assert news_celtics()

    def test_parse_bot_user(self):
        assert parse_bot_user(69332752)

    def test_get_photos(self):
        assert get_photos(69332752)

    def test_search_country_for_db(self):
        assert search_country_for_db()

    def test_search_city_for_db(self):
        assert search_city_for_db(1)

    def test_search_users(self):
        search_users(18, 20, 1, 1, 1, 1)

    def teardown_class(self):
        print("method teardown")


