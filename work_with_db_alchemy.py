from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config_keys import owner_db, db_name, db_password
from need_functions_modules import search_country_for_db, search_city_for_db

engine = create_engine(f"postgresql+psycopg2://{owner_db}:{db_password}@localhost:5432/{db_name}")

Session = sessionmaker(bind=engine)
session = Session()

BASE = declarative_base()


class Gender(BASE):
    __tablename__ = "user_gender"

    ID = Column(Integer, primary_key=True)
    title = Column(String(20))


class County(BASE):
    __tablename__ = "user_country"

    ID = Column(Integer, primary_key=True)
    name = Column(String(50))


class Town(BASE):
    __tablename__ = "user_town"

    ID = Column(Integer, primary_key=True)
    name = Column(String)
    country_id = Column(Integer)


class Status(BASE):
    __tablename__ = "user_status"

    ID = Column(Integer, primary_key=True)
    name = Column(String)


class AllVkUsers(BASE):
    __tablename__ = "all_vk_users"

    vk_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    gender_id = Column(Integer, ForeignKey("user_gender.ID"))
    country_id = Column(Integer, ForeignKey("user_country.ID"))
    town_id = Column(Integer, ForeignKey("user_town.ID"))
    status_id = Column(Integer, ForeignKey("user_status.ID"))
    is_bot_user = Column(Boolean, default=False)


class SearchParams(BASE):
    __tablename__ = "search_params"

    ID = Column(Integer, primary_key=True)
    search_owner_id = Column(Integer, ForeignKey("all_vk_users.vk_id"))
    age_from = Column(Integer)
    age_to = Column(Integer)
    status = Column(Integer, ForeignKey("user_status.ID"))
    town = Column(Integer, ForeignKey("user_town.ID"))
    country = Column(Integer, ForeignKey("user_country.ID"))
    gender = Column(Integer, ForeignKey("user_gender.ID"))


class SearchUsers(BASE):
    __tablename__ = "search_users"

    ID = Column(Integer, primary_key=True)
    search_params_id = Column(Integer, ForeignKey("search_params.ID"))
    found_result_vk_id = Column(Integer, ForeignKey("all_vk_users.vk_id"))
    is_shown = Column(Boolean, default=False)
    liked_status = Column(Boolean, nullable=True)


def insert_into_gender():
    gender_woman = Gender(ID=1, title="woman")
    gender_man = Gender(ID=2, title="man")
    gender_any = Gender(ID=3, title="any")
    session.add_all([gender_woman, gender_man, gender_any])
    session.commit()


def insert_into_status():
    status_1 = Status(ID=1, name="не женат(не за мужем)")
    status_2 = Status(ID=2, name="встречается")
    status_3 = Status(ID=3, name="помолвлен(-а)")
    status_4 = Status(ID=4, name="женат(за мужем)")
    status_5 = Status(ID=5, name="всё сложно")
    status_6 = Status(ID=6, name="в активном поиске")
    status_7 = Status(ID=7, name="влюблен(-а)")
    status_8 = Status(ID=8, name="в гражданском браке")
    session.add_all([status_1, status_2, status_3, status_4, status_5, status_6, status_7, status_8])
    session.commit()


def insert_into_country():
    countrys = search_country_for_db()
    for i in countrys:
        add = County(ID=i["id"], name=i["title"])
        session.add(add)
    session.commit()


def insert_into_cities():
    select_country = session.query(County).all()
    for i in select_country:
        city = search_city_for_db(i.ID)
        for a in city:
            city_id = a["id"]
            city_title = a["title"]
            add = Town(ID=city_id, name=city_title, country_id=i.ID)
            session.add(add)
            session.commit()


def insert_bot_user_to_vk_users(vk_id, first_name, last_name, gender):
    one_user = session.query(AllVkUsers).filter(vk_id == AllVkUsers.vk_id).first()
    know_user_gender = session.query(Gender).filter(gender == Gender.ID).first()
    if one_user:
        one_user.vk_id = vk_id
        one_user.name = first_name
        one_user.surname = last_name
        one_user.gender_id = know_user_gender.ID
        one_user.is_bot_user = True
        session.commit()
    else:
        insert_like_bot_user = AllVkUsers(vk_id=vk_id, name=first_name, surname=last_name, is_bot_user=True,
                                          gender_id=know_user_gender.ID)
        session.add(insert_like_bot_user)
        session.commit()


def select_search_country(country):
    search_country_from_db = session.query(County).filter(country.capitalize() == County.name).first()
    some_dict = {}
    if search_country_from_db:
        some_dict["ID"] = search_country_from_db.ID
        some_dict["name"] = search_country_from_db.name
        return some_dict
    else:
        return False


def check_town(country_id, town_name):
    new_town = session.query(Town).filter(and_(
        country_id == Town.country_id, town_name.capitalize() == Town.name
    )).first()
    some_dict = {}
    if new_town:
        some_dict["ID"] = new_town.ID
        some_dict["name"] = new_town.name
        return some_dict
    else:
        return False


def insert_search_params(vk_id, age_from_param, age_to_param, status_param, town_name, country_id, gender_id):
    new_status_param = session.query(Status).filter(status_param == Status.ID).first()
    select_country = session.query(County).filter(country_id == County.ID).first()
    select_gender = session.query(Gender).filter(gender_id == Gender.ID).first()
    check_params = session.query(SearchParams).filter(SearchParams.search_owner_id == vk_id,
                                                      ).first()
    if check_params:
        check_params.search_owner_id = vk_id
        check_params.age_from = age_from_param
        check_params.age_to = age_to_param
        check_params.status = new_status_param.ID
        check_params.town = town_name
        check_params.country = select_country.ID
        check_params.gender = select_gender.ID
        session.commit()
    else:
        add_params = SearchParams(search_owner_id=vk_id, age_from=age_from_param, age_to=age_to_param,
                                  status=new_status_param.ID,
                                  town=town_name, country=select_country.ID, gender=select_gender.ID)
        session.add(add_params)
        session.commit()


def insert_searched_users_to_all_vk_users(user_vk_id, user_name, user_surname, user_gender_id,
                                          user_country_id, user_town_id, user_status_id):
    one_user = session.query(AllVkUsers).filter(user_vk_id == AllVkUsers.vk_id).first()
    know_gender = session.query(Gender).filter(user_gender_id == Gender.ID).first()
    know_country = session.query(County).filter(user_country_id == County.ID).first()
    know_town = session.query(Town).filter(user_town_id == Town.ID).first()
    know_status = session.query(Status).filter(user_status_id == Status.ID).first()
    if one_user:
        one_user.vk_id = user_vk_id
        one_user.name = user_name
        one_user.surname = user_surname
        one_user.gender_id = know_gender.ID
        one_user.country_id = know_country.ID
        one_user.town_id = know_town.ID
        one_user.status_id = know_status.ID
        session.commit()
    else:
        add = AllVkUsers(vk_id=user_vk_id, name=user_name, surname=user_surname, gender_id=know_gender.ID,
                         country_id=know_country.ID, town_id=know_town.ID, status_id=know_status.ID)
        session.add(add)
        session.commit()


def insert_searched_users(bot_user_vk_id, searched_user_vk_id):
    check_users_from_params = session.query(SearchParams).filter(bot_user_vk_id == SearchParams.search_owner_id).first()
    check_users_from_all_users = session.query(AllVkUsers).filter(searched_user_vk_id == AllVkUsers.vk_id).first()
    check_user_in = session.query(SearchUsers).filter(SearchUsers.found_result_vk_id == searched_user_vk_id).first()
    if check_user_in:
        check_user_in.found_result_vk_id = check_users_from_all_users.vk_id
        check_user_in.search_params_id = check_users_from_params.ID
        session.commit()
    else:
        add = SearchUsers(search_params_id=check_users_from_params.ID,
                          found_result_vk_id=check_users_from_all_users.vk_id)
        session.add(add)
        session.commit()


def select_searched_users_for_bot_users(bot_user_vk_id):
    check_users_from_params = session.query(SearchParams).filter(bot_user_vk_id == SearchParams.search_owner_id).first()
    check_users_from_found_result = session.query(SearchUsers).filter(
        check_users_from_params.ID == SearchUsers.search_params_id
    ).first()
    return check_users_from_found_result


def set_like_status_and_show_status(searched_user_id):
    set_user = session.query(SearchUsers).filter(searched_user_id == SearchUsers.found_result_vk_id).first()
    set_user.is_shown = True
    set_user.liked_status = True
    session.commit()


def set_hate_status_and_show_status(searched_user_id):
    set_user = session.query(SearchUsers).filter(searched_user_id == SearchUsers.found_result_vk_id).first()
    set_user.is_shown = True
    set_user.liked_status = False
    session.commit()


def select_to_user_all_liked_users(owner_vk_id):
    check_users_from_params = session.query(SearchParams).filter(owner_vk_id == SearchParams.search_owner_id).first()
    check_users_from_found_result = session.query(SearchUsers).filter(
        SearchUsers.search_params_id == check_users_from_params.ID,
        SearchUsers.liked_status == True
    ).all()
    return check_users_from_found_result


def select_to_user_all_hated_users(owner_vk_id):
    check_users_from_params = session.query(SearchParams).filter(owner_vk_id == SearchParams.search_owner_id).first()
    check_users_from_found_result = session.query(SearchUsers).filter(
        SearchUsers.search_params_id == check_users_from_params.ID,
        SearchUsers.liked_status == False
    ).all()
    return check_users_from_found_result


if __name__ == "__main__":
    pass
