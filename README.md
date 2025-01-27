# ms-memessaging

```
from app.database import Base
from app.database import DATABASE_URL

# Configurar metadata, por defecto es None
target_metadata = Base.metadata

# Configurar conexión a la base de datos
config.set_main_option("sqlalchemy.url", DATABASE_URL)
```

alembic init alembic
alembic init -t async alembic

alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

uvicorn app.main:app --reload
uvicorn app.main:app --reload --port 8000
uvicorn app.websocket.websocket:app --host 0.0.0.0 --port 8001 --reload
