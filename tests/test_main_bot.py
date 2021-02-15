import pytest
from main_bot import ServerBot
from config_keys import user_token, bots_token


class Testmainbot:
    def setup_class(self):
        print("setup class")

    def test_hello(self):
        user = ServerBot(user_token, bots_token)
        assert user.hello()

    def test_searching(self):
        user = ServerBot(user_token, bots_token)
        assert user.searching()

    def test_selecting_country(self):
        user = ServerBot(user_token, bots_token)
        assert user.selecting_country()

    def test_select_city(self):
        user = ServerBot(user_token, bots_token)
        assert user.select_city()

    def test_talking(self):
        user = ServerBot(user_token, bots_token)
        assert user.talking()

    def teardown_class(self):
        print("teardown class")
