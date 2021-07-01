import os


user_token = os.getenv("USER_TOKEN")
bots_token = os.getenv("BOTS_TOKEN")
owner_db = os.getenv("POSTGRES_USER", "owner_pro_diplom_db")
db_password = os.getenv("POSTGRES_PASSWORD", "owner_pro_diplom_db")
db_name = os.getenv("POSTGRES_DB", "pro_diplom_db")
