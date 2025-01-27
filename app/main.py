from fastapi import FastAPI

from app.routers import chats, messages

app = FastAPI()

# Incluir los routers directamente
app.include_router(chats.router, prefix="/chats", tags=["Chats"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Chat API!"}
