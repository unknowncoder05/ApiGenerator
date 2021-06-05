pass a json file as input and get a formal functional and secure api


```json
{
    "settings": {
        "name": "epic_app",
        "framework": "python/django"
    },
    "database": [{
        "type": "POSTGRES",
        "identifier": "maindb",
        "__host": "DB_HOST",
        "__password": "DB_PASSWORD",
        "__db": "DB_DB",
        "__user": "DB_USERS"

    }],
    "models": {
        "user": {
            "__extends": "USER",
            "__db": "maindb"
        },
        "movie": {
            "title": { "type": "string", "min": 4, "max": 20, "required": true },
            "description": { "type": "string", "min": 30, "max": 200 },
            "duration": { "type": "time", "min": 900, "max": 2400, "required": true },
            "__actions": {
                "public": ["list", "get"],
                "authenticated": ["list", "get"],
                "owner": ["all"]
            },
            "__db": "maindb"
        }
    },
    "deploy": {
        "far": "far future"
    }
}
```