def up(db):
    """Creates the multiagent collection with schema validation.

    Args:
        db: The MongoDB database instance.
    """
    # Create collection with schema validator
    db.create_collection(
        "multiagent",
        validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["id", "prompt", "status", "created_at", "updated_at"],
                "properties": {
                    "id":         {"bsonType": "string"},
                    "prompt":     {"bsonType": "string"},
                    "status":     {"bsonType": "string", "enum": ["pending", "running", "done", "error"]},
                    "result":     {"bsonType": ["string", "null"]},
                    "created_at": {"bsonType": "string"},
                    "updated_at": {"bsonType": "string"},
                },
            }
        },
    )
    # Enforce unique run IDs
    db["multiagent"].create_index("id", unique=True)
