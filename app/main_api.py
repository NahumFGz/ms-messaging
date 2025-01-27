from fastapi import FastAPI

from app.api import chats, messages

# Crear la aplicación FastAPI para la API REST
app_api = FastAPI()

# Incluir las rutas de la API
app_api.include_router(chats.router, prefix="/chats", tags=["Chats"])
app_api.include_router(messages.router, prefix="/messages", tags=["Messages"])


# Endpoint de bienvenida
@app_api.get("/")
async def root():
    return {"message": "Welcome to the Chat API!"}


# # Ejecutar la API REST en el puerto 8000
# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app_api, host="0.0.0.0", port=8000)
