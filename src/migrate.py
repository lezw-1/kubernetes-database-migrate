import importlib
import os
from pathlib import Path

from pymongo import MongoClient

_CLIENT = MongoClient(os.environ["MONGO_URL"])
_MIGRATIONS_COLLECTION = "_migrations"


def _run_for(db_name: str):
    """Run pending migrations for a given database.

    Args:
        db_name: The MongoDB database name (matches the migrations subdirectory).
    """
    db = _CLIENT[db_name]
    applied = {
        doc["name"]
        for doc in db[_MIGRATIONS_COLLECTION].find({}, {"name": 1})
    }

    migration_dir = Path(__file__).parent / "migrations" / db_name
    migration_files = sorted(migration_dir.glob("[0-9]*.py"))

    for path in migration_files:
        name = path.stem
        if name in applied:
            continue
        module = importlib.import_module(f"migrations.{db_name}.{name}")
        module.up(db)
        db[_MIGRATIONS_COLLECTION].insert_one({"name": name})
        print(f"[{db_name}] Applied migration: {name}")


if __name__ == "__main__":
    # Run all migrations for all databases
    _run_for("agent")
    _run_for("multiagent")
