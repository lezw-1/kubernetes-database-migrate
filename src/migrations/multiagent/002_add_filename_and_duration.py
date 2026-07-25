def up(db):
    """Add filename and duration_seconds fields to the multiagent collection schema.

    Args:
        db: The MongoDB database instance.
    """
    db.command({
        "collMod": "multiagent",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["id", "prompt", "status", "created_at", "updated_at"],
                "properties": {
                    "id":               {"bsonType": "string"},
                    "prompt":           {"bsonType": "string"},
                    "filename":         {"bsonType": ["string", "null"]},
                    "status":           {"bsonType": "string", "enum": ["pending", "running", "done", "error"]},
                    "result":           {"bsonType": ["string", "null"]},
                    "duration_seconds": {"bsonType": ["double", "null"]},
                    "created_at":       {"bsonType": "string"},
                    "updated_at":       {"bsonType": "string"},
                },
            }
        },
    })
