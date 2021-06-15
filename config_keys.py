import os


user_token = os.getenv("USER_TOKEN", "6ab3320f1ce920509d1c882704c9ac2bc186aa181a335b8d2bba5d13b5ae758f1266bd432ee9b779688ff")
bots_token = os.getenv("BOTS_TOKEN", "ed8e88703b96c5fd0b77dbb37fe2d76113a49ccfd7639d66214da340a22d98741185dad363f6d79661da8")
owner_db = os.getenv("POSTGRES_USER", "owner_pro_diplom_db")
db_password = os.getenv("POSTGRES_PASSWORD", "owner_pro_diplom_db")
db_name = os.getenv("POSTGRES_DB", "pro_diplom_db")
