config = {
    "dirs": {
        "logger": "api.log",
        "docs": "docs/openapi.yaml"
    },
    "db": {
        "dbname": "postgres",
        "user": "postgres",
        "password": "1234",
        "host": "database",  # "localhost"
        "port": "5432",  # "5442"
    },
    "docs": {
        "url": "/docs",
        "enable": True,
    },
    "web": {
        "port": 8888,
    }
}
