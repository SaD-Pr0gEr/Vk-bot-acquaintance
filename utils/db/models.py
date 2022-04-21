from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from config import BASE

__all__ = (
    "Gender",
    "County",
    "Town",
    "Status",
    "AllVkUsers",
    "SearchParams",
    "SearchUsers"
)


class Gender(BASE):
    __tablename__ = "user_gender"

    ID = Column(Integer, primary_key=True)
    titles = Column(
        String(20)
    )


class County(BASE):
    __tablename__ = "user_country"

    ID = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class Town(BASE):
    __tablename__ = "user_town"

    ID = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country_id = Column(Integer, nullable=False)


class Status(BASE):
    __tablename__ = "user_status"

    ID = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class AllVkUsers(BASE):
    __tablename__ = "all_vk_users"

    vk_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    gender_id = Column(Integer, ForeignKey("user_gender.ID"))
    country_id = Column(Integer, ForeignKey("user_country.ID"))
    town_id = Column(Integer, ForeignKey("user_town.ID"))
    status_id = Column(Integer, ForeignKey("user_status.ID"))
    is_bot_user = Column(
        Boolean,
        default=False,
        nullable=False
    )


class SearchParams(BASE):
    __tablename__ = "search_params"

    ID = Column(Integer, primary_key=True)
    search_owner_id = Column(Integer, ForeignKey("all_vk_users.vk_id"))
    age_from = Column(Integer, nullable=False)
    age_to = Column(Integer, nullable=False)
    status = Column(Integer, ForeignKey("user_status.ID"))
    town = Column(Integer, ForeignKey("user_town.ID"))
    country = Column(Integer, ForeignKey("user_country.ID"))
    gender = Column(Integer, ForeignKey("user_gender.ID"))


class SearchUsers(BASE):
    __tablename__ = "search_users"

    ID = Column(Integer, primary_key=True)
    search_params_id = Column(Integer, ForeignKey("search_params.ID"))
    found_result_vk_id = Column(Integer, ForeignKey("all_vk_users.vk_id"))
    is_shown = Column(
        Boolean,
        default=False,
        nullable=False
    )
    liked_status = Column(
        Boolean,
        nullable=False,
        default=False
    )
