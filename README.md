# Vkinder бот для знакомств ВКонтакте
Бот для сообщества который ищет пользователей с ВК и выводит топ 3 
фотографии и ссылку на профиль найденного пользователя! Также отметит 
их как `лайкнутый` или как `хейтед` пользователи! Все данные записываются 
в базу данных! Также бот может найти новости про баскетбол и информацию
с `Wikipedia` про разных команд. Но это вы можете убрать)

## Что необходимо знать для работы с проектом
* Python
* Pytest
* BeautifulSoup
* Postgresql
* SQLAlchemy
* VK-Api

## Для развёртывания проекта
* Docker(Docker-compose)

## Как работать с проектом 
### Установка и настройка зависимости
* Устанавливаем зависимости с командой `pip install -r requirements.txt`
* Создаёи файл `.env` 
* Добавим туда наш `APP_ID` с ВК для сообщества(APP_ID=your-app-id)
* Добавим наш `USER_TOKEN` с ВК(USER_TOKEN=your-user-token). **Обратите внимание!** 
Для получение токена можете использовать функцию get_token(в файле need_functions_modules.py)
* Наконец то добавьте токен бота `BOTS_TOKEN`(BOTS_TOKEN=your-community-token
 создаёте токен для сообщества)
 
### Работа с базой данных
* Для этого сначала замените хост c pro_diplom_db_1 на localhost в конфгиах подключение к базе(файл 
`work_with_db_alchemy.py`, строка 7)
* Запускаем файл `work_with_db_alchemy.py` и все таблицы создаются в базе 
* И наконец запускаем сам проект(запускайте файл `main_bot.py`)

### Развёртывание проекта на Docker 
* Теперь замените хост c localhost на pro_diplom_db_1 в конфгиах подключение к базе(файл 
`work_with_db_alchemy.py`, строка 7)
* Запускайте команду `Docker compose build`
* И наконец запускаем `Docker compose up`

Но это ещё не всё! Теперь нам надо повторить те же самые настройки для запуска проекта! 
* Набираем команду `Docker exec -it pro_diplom_bot_1 bash` и внутри баш консоли запускаем 
команду `work_with_db_alchemy.py` чтобы создать таблицы.
Теперь всё работает и можете наслаждаться) Вот такие вот пироги) Удачи в проектах! 
