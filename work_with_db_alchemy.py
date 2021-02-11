from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, and_, Boolean, null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config_keys import owner_db, db_name, db_password
from need_functions_modules import search_country_for_db

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
    liked_status = Column(Boolean, default=null)


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
        know_user_gender = session.query(Gender).filter(gender == Gender.ID).first()
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


def check_town(town_id, town_name):
    new_town = session.query(Town).filter(town_id == Town.ID).first()
    if new_town:
        Town.ID = new_town.ID
        Town.name = new_town.name
        session.commit()

    else:
        add_town = Town(ID=town_id, name=town_name)
        session.add(add_town)
        session.commit()


def insert_search_params(vk_id, age_from_param, age_to_param, status_param, town_id, country_id, gender_id):
    new_status_param = session.query(Status).filter(status_param == Status.ID).first()
    select_country = session.query(County).filter(country_id == County.ID).first()
    select_gender = session.query(Gender).filter(gender_id == Gender.ID).first()
    check_params = session.query(SearchParams).filter(and_(SearchParams.search_owner_id == vk_id,
                                                           SearchParams.age_from == age_from_param,
                                                           SearchParams.age_to == age_to_param,
                                                           SearchParams.status == new_status_param.ID,
                                                           SearchParams.town == town_id,
                                                           SearchParams.country == select_country.ID,
                                                           SearchParams.gender == select_gender.ID))
    if check_params:
        SearchParams.search_owner_id = vk_id
        SearchParams.age_from = age_from_param
        SearchParams.age_to = age_to_param
        SearchParams.status = new_status_param.ID
        SearchParams.town = town_id
        SearchParams.country = select_country.ID
        SearchParams.gender = select_gender.ID
        session.commit()
    else:
        add_params = SearchParams(search_owner_id=vk_id, age_from=age_from_param, age_to=age_to_param,
                                  status=new_status_param.ID,
                                  town=town_id, country=select_country.ID, gender=select_gender.ID)
        session.add(add_params)
        session.commit()


if __name__ == "__main__":
    check_town(19, "chirchik")
    insert_search_params(616586034, 232, 343, 3, 19, 1, 1)
    # insert_bot_user_to_vk_users(616586034, "Озод", "ochilov", 1)
    # insert_into_country()
    # BASE.metadata.create_all(engine)
    # insert_into_gender()
    # insert_into_status()
    pass
