import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from config import USER_TOKEN, BOT_TOKEN
from need_functions_modules import info_celtics_wiki as i_s_w, news_celtics as n_c, search_users, parse_bot_user, \
    get_photos
from work_with_db_alchemy import insert_bot_user_to_vk_users, select_search_country, insert_search_params, \
    insert_searched_users_to_all_vk_users, select_searched_users_for_bot_users, insert_searched_users, \
    set_like_status_and_show_status, set_hate_status_and_show_status, select_to_user_all_hated_users, \
    select_to_user_all_liked_users, check_town

STATUSES = dict(hello=0, commands=1, choose_gender=2, choose_age_from=3, choose_age_to=4,
                choose_status=5, news=6, history=7, got_it=8,
                choose_country_wait=9, choose_city_wait=10, wait_database=11, like_wait=12,
                select_users=13, wait_like=14, wait_likekist_or_hatelist=15
                )


class User:

    def __init__(self, user_id=616586034, user_name: str = "ozod",
                 user_surname: str = "ochilov", user_gender: str = "man", age_from: int = 1,
                 age_to: int = 10, country_id: int = 1, country_name: str = "россия", town: str = "москва",
                 town_id: int = 1, status=1, gender=1, gender_text=""):
        self.user_id = user_id
        self.user_name = user_name
        self.user_surname = user_surname
        self.user_gender = user_gender
        self.age_from = age_from
        self.age_to = age_to
        self.country_name = country_name
        self.country_id = country_id
        self.town = town
        self.town_id = town_id
        self.status = status
        self.gender = gender
        self.gender_text = gender_text


class ServerBot:

    def __init__(self, need_params, users_token, group_token, give_found_result=0):
        self.vk = vk_api.VkApi(token=group_token)
        self.users_token = users_token
        self.long_poll = VkLongPoll(self.vk)
        self.request = ''
        self.state = STATUSES["hello"]
        self.give_found_result = give_found_result
        self.need_params = need_params

    def send_msg(self, user_id, message):
        self.vk.method("messages.send", {'user_id': user_id, 'message': message, "random_id": randrange(10 ** 7)
                                         })

    def send_photo(self, user_id, message, owner_photo_id, photo_id):
        self.vk.method("messages.send", {'user_id': user_id, 'message': message, "random_id": randrange(10 ** 7),
                                         "attachment": f"photo{owner_photo_id}_{photo_id}"})

    def hello(self):
        parsing_bot_user = parse_bot_user(self.need_params.user_id)
        self.need_params.user_name = parsing_bot_user["name"]
        self.need_params.user_surname = parsing_bot_user["surname"]
        self.need_params.user_gender = parsing_bot_user["gender"]
        self.send_msg(self.need_params.user_id, f"Привет {self.need_params.user_name}!\n"
                                                f"Я бот VKinder ваш помощник для помощи вводите bot_commands")
        insert_bot_user_to_vk_users(self.need_params.user_id, self.need_params.user_name, self.need_params.user_surname,
                                    self.need_params.user_gender)
        self.state = STATUSES["commands"]
        return self.state

    def commands(self):
        return self.send_msg(self.need_params.user_id,
                             f"Выберите команду:\n"
                             f"Search_users: Искать людей для знакомства\n"
                             f"News: Новости про команды Boston Celtics\n"
                             f"History: История команды Boston Celtics и прочие материалы")

    def searching(self):
        search = search_users(self.need_params.age_from, self.need_params.age_to, self.need_params.gender,
                              self.need_params.town, self.need_params.status, self.need_params.country_id)
        for i in search:
            username = i["name"]
            surname = i["surname"]
            vk_id = i["User_ID"]
            city_id = i["city"]["id"]
            country_id = i["country"]["id"]
            gender_id = i["gender"]
            insert_searched_users_to_all_vk_users(vk_id, username, surname, gender_id, country_id,
                                                  city_id, self.need_params.status)
            insert_searched_users(self.need_params.user_id, vk_id)
        self.state = STATUSES["select_users"]
        return search

    def selecting_country(self):
        searching = select_search_country(self.need_params.country_name)
        if searching:
            self.need_params.country_id = searching["ID"]
            self.need_params.country_name = searching["name"]
            self.state = STATUSES["choose_city_wait"]
            self.send_msg(self.need_params.user_id, f"Вводите город поиска")
            return self.state
        else:
            self.send_msg(self.need_params.user_id, "Вы ввели неправильную страну пожалуйста вводите её заново")
            self.state = STATUSES["choose_country_wait"]
            return self.state

    def select_city(self):
        searching = check_town(self.need_params.country_id, self.need_params.town)
        if searching:
            self.need_params.town_id = searching["ID"]
            self.need_params.town = searching["name"]
            self.state = STATUSES["choose_gender"]
            self.send_msg(self.need_params.user_id, f"вводите пол юзера:\n"
                                                    f"man - мужчина\n"
                                                    f"woman - женщина\n"
                                                    f"any - без разницы")
            return self.state
        else:
            self.send_msg(self.need_params.user_id,
                          f"Вы ввели неправильный город поиска! пожалуйста вводите её заново)\n"
                          f" Постарайтесь вводить известные города")
            self.state = STATUSES["choose_city_wait"]
            return self.state

    def news(self):
        for news in n_c():
            self.send_msg(self.need_params.user_id, news)
        self.send_msg(self.need_params.user_id, "Этот сеанс окончен и мы возвращаемся в состояние bot_commands")
        self.state = STATUSES["commands"]
        self.commands()

    def history(self):
        self.send_msg(self.need_params.user_id, i_s_w())
        self.send_msg(self.need_params.user_id, "Этот сеанс окончен и мы возвращаемся в состояние bot_commands")
        self.state = STATUSES["commands"]
        self.commands()

    def got_it(self):
        self.state = STATUSES["got_it"]
        self.send_msg(self.need_params.user_id, f'Параметры поиска вашей половинки:\n'
                                                f'Минимальный возраст: {self.need_params.age_from},\n'
                                                f'Максимальный возраст: {self.need_params.age_to},\n'
                                                f'Город: {self.need_params.town},\n'
                                                f'Пол: {self.need_params.gender_text},\n'
                                                f'Страна: {self.need_params.country_name},\n'
                                                f'Семейное положение: {self.need_params.status}\n'
                                                f'Хотите начать?\n'
                                                f'пишите да или нет')
        return self.state

    def show_searched_users(self):
        self.give_found_result = select_searched_users_for_bot_users(self.need_params.user_id)
        self.send_msg(self.need_params.user_id, f"vk.com/id{self.give_found_result.found_result_vk_id}")
        photos = get_photos(self.give_found_result.found_result_vk_id)
        self.send_msg(self.need_params.user_id, "Топ 3 фотографии юзера:\n ")
        for a in photos:
            self.send_photo(self.need_params.user_id, " ", self.give_found_result.found_result_vk_id,
                            a["ID"])
        self.send_msg(self.need_params.user_id,
                      "Нравится? если да то пишите like если нет то hate! для выхода пишите quit\n",
                      )
        self.state = STATUSES["wait_like"]
        return self.give_found_result

    def show_all_liked_users(self):
        liked_users = select_to_user_all_liked_users(self.need_params.user_id)
        for i in liked_users:
            self.send_msg(self.need_params.user_id, f"vk.com/id{i.found_result_vk_id}")
            photos = get_photos(i.found_result_vk_id)
            for a in photos:
                self.send_photo(self.need_params.user_id, " ", i.found_result_vk_id, a["ID"])
        self.send_msg(self.need_params.user_id, "Этот сеанс окончен и мы вернёмся в состояние Commands")
        self.state = STATUSES["commands"]
        self.commands()

    def show_all_hated_users(self):
        hated_users = select_to_user_all_hated_users(self.need_params.user_id)
        for i in hated_users:
            self.send_msg(self.need_params.user_id, f"vk.com/id{i.found_result_vk_id}")
            photos = get_photos(i.found_result_vk_id)
            for a in photos:
                self.send_photo(self.need_params.user_id, " ", i.found_result_vk_id,
                                a["ID"])
        self.send_msg(self.need_params.user_id, "Этот сеанс окончен и мы вернёмся в состояние Commands")
        self.state = STATUSES["commands"]
        self.commands()

    def talking(self):
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    self.request = event.text.lower()
                    self.need_params.user_id = event.user_id

                    if self.request == "привет" and self.state == STATUSES["hello"]:
                        self.hello()

                    elif self.request == "привет" and self.state == STATUSES["commands"]:
                        self.send_msg(self.need_params.user_id,
                                      f"Мы же уже поздаровались) давай лучше выбери команду)\n")
                        self.commands()

                    elif self.request == "bot_commands" and self.state == STATUSES["commands"]:
                        self.state = STATUSES["commands"]
                        self.commands()

                    elif self.request == "search_users" and self.state == STATUSES["commands"]:
                        self.state = STATUSES["choose_country_wait"]
                        self.send_msg(self.need_params.user_id,
                                      f"ВНИМАНИЯ! предупреждаю вас о том когда вы наберёте не правильную"
                                      f" команду или не правильно вводите параметры поиска то это в конце"
                                      f" концов повлияет на ваш же поиск и вы не получите нужный ответ и "
                                      f"мы снова возвращаемся в bot_commands!\n"
                                      f"Поэтому просим вас быть внимательнее и правильно заполнить нужные"
                                      f" поля! спасибо за понимание)\n"
                                      f"Ну а теперь приступим к поиску)\n"
                                      f"Вводите страну поиска Например Россия, Украина, Белорусия и т.д.\n")

                    elif self.state == STATUSES["choose_country_wait"]:
                        self.need_params.country_name = self.request
                        self.selecting_country()

                    elif self.state == STATUSES["choose_city_wait"]:
                        self.need_params.town = self.request
                        self.select_city()

                    elif self.request == "man" and self.state == STATUSES["choose_gender"]:
                        self.need_params.gender = 2
                        self.need_params.gender_text = "man"
                        self.state = STATUSES["choose_age_from"]
                        self.send_msg(self.need_params.user_id, f"Вводите минимальный возраст пользователя "
                                                                f"от 10 до 100")

                    elif self.request == "woman" and self.state == STATUSES["choose_gender"]:
                        self.need_params.gender = 1
                        self.need_params.gender_text = "woman"
                        self.state = STATUSES["choose_age_from"]
                        self.send_msg(self.need_params.user_id, f"Вводите минимальный возраст пользователя "
                                                                f"от 10 до 100")

                    elif self.request == "any" and self.state == STATUSES["choose_gender"]:
                        self.need_params.gender = 0
                        self.need_params.gender_text = "any"
                        self.state = STATUSES["choose_age_from"]
                        self.send_msg(self.need_params.user_id, f"Вводите минимальный возраст пользователя "
                                                                f"от 10 до 100")

                    elif self.state == STATUSES["choose_age_from"] and int(self.request) in range(100):
                        self.state = STATUSES["choose_age_to"]
                        self.need_params.age_from = self.request
                        self.send_msg(self.need_params.user_id, f"Вводите максимальный возраст пользователя"
                                                                f" и оно не должно быть меньше минимального возраста")

                    elif self.state == STATUSES["choose_age_to"] and int(self.request) in range(100):
                        self.state = STATUSES["choose_status"]
                        self.need_params.age_to = self.request
                        self.send_msg(self.need_params.user_id, f"Вводите номер статуса пользователя:\n"
                                                                f"1.не женат(не за мужем)\n"
                                                                f"2.встречается\n"
                                                                f"3.помолвлен(-а)\n"
                                                                f"4.женат(за мужем)\n"
                                                                f"5.всё сложно\n"
                                                                f"6.в активном поиске\n"
                                                                f"7.влюблен(-а)\n"
                                                                f"8.в гражданском браке")

                    elif self.state == STATUSES["choose_status"] and self.request == "1":
                        self.need_params.status = 1
                        self.got_it()

                    elif self.state == STATUSES["choose_status"] and self.request == "2":
                        self.need_params.status = 2
                        self.got_it()

                    elif self.state == STATUSES["choose_status"] and self.request == "3":
                        self.need_params.status = 3
                        self.got_it()

                    elif self.state == STATUSES["choose_status"] and self.request == "4":
                        self.need_params.status = 4
                        self.got_it()

                    elif self.state == STATUSES["choose_status"] and self.request == "5":
                        self.need_params.status = 5
                        self.got_it()

                    elif self.state == STATUSES["choose_status"] and self.request == "6":
                        self.need_params.status = 6
                        self.got_it()

                    elif self.state == STATUSES["choose_status"] and self.request == "7":
                        self.need_params.status = 7
                        self.got_it()

                    elif self.state == STATUSES["choose_status"] and self.request == "8":
                        self.need_params.status = 8
                        self.got_it()

                    elif self.state == STATUSES["got_it"] and self.request.lower() == "да":
                        insert_search_params(self.need_params.user_id, self.need_params.age_from,
                                             self.need_params.age_to, self.need_params.status,
                                             self.need_params.town_id, self.need_params.country_id,
                                             self.need_params.gender)
                        self.searching()
                        self.show_searched_users()

                    elif self.state == STATUSES["got_it"] and self.request.lower() == "нет":
                        self.send_msg(self.need_params.user_id,
                                      f"Вы выбрали команду нет поэтому мы возвращаемся в состояние Сommands")
                        self.state = STATUSES["commands"]
                        self.commands()

                    elif self.state == STATUSES["wait_like"] and self.request == "like":
                        set_like_status_and_show_status(self.give_found_result.found_result_vk_id)
                        self.state = STATUSES["wait_like"]
                        self.show_searched_users()

                    elif self.state == STATUSES["wait_like"] and self.request == "hate":
                        set_hate_status_and_show_status(self.give_found_result.found_result_vk_id)
                        self.state = STATUSES["wait_like"]
                        self.show_searched_users()

                    elif self.state == STATUSES["wait_like"] and self.request == "quit":
                        self.send_msg(self.need_params.user_id, f"хотите ли смотреть список лайкнутых или чёрный "
                                                                f"список?)\n "
                                                                f"Если да то пишите like_list или hate_list или exit "
                                                                f"для выхода")
                        self.state = STATUSES["wait_likekist_or_hatelist"]

                    elif self.state == STATUSES["wait_likekist_or_hatelist"] and self.request == "like_list":
                        self.show_all_liked_users()

                    elif self.state == STATUSES["wait_likekist_or_hatelist"] and self.request == "hate_list":
                        self.show_all_hated_users()

                    elif self.state == STATUSES["wait_likekist_or_hatelist"] and self.request == "exit":
                        self.state = STATUSES["commands"]
                        self.send_msg(self.need_params.user_id,
                                      f"Этот сеанс окончен и мы вернёмся в состояние Commands")
                        self.commands()

                    elif self.request == "news" and self.state == STATUSES["commands"]:
                        self.news()

                    elif self.request == "history" and self.state == STATUSES["commands"]:
                        self.history()

                    else:
                        self.send_msg(self.need_params.user_id, f"ERROR! Вы набрали не правильную команду или где то "
                                                                f"допустили ошибку! поэтому вернёмся в Hello")
                        self.state = STATUSES["hello"]
                        self.hello()


if __name__ == "__main__":
    user = User()
    some_user = ServerBot(user, USER_TOKEN, BOT_TOKEN)
    some_user.talking()
