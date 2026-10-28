
import os
import sqlite3

from flask import current_app, g


def get_db():
    if "db" not in g:
        database_path = current_app.config["DATABASE"]

        parent_directory = os.path.dirname(database_path)
        if parent_directory:
            os.makedirs(parent_directory, exist_ok=True)

        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    schema_path = os.path.join(
        os.path.dirname(__file__),
        "schema.sql"
    )

    with open(schema_path, "r", encoding="utf-8") as schema_file:
        db.executescript(schema_file.read())

    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
