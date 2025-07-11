TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["users.models"],
            "models": ["users.models","products.models"],
            "default_connection": "default",
        }
    }
}
