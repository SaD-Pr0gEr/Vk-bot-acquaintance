import json

from sqlalchemy import create_engine, MetaData

from config import DATABASE_URL, BASE_DIR


def dump_data():
    engine = create_engine(DATABASE_URL)
    meta = MetaData()
    meta.reflect(bind=engine)
    result = {}
    for table in meta.sorted_tables:
        result[table.name] = [dict(row) for row in engine.execute(table.select())]
    return result


def save_dump_data(data: dict):
    file_path = str(BASE_DIR / "dump.json")
    with open(file_path, encoding="utf-8", mode="w") as file:
        json.dump(data, file, indent=4)
    return file_path
