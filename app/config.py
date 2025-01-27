from decouple import config

DATABASE_URL = (
    f"postgresql+asyncpg://{config('DB_USERNAME')}:{config('DB_PASSWORD')}"
    f"@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"
)
