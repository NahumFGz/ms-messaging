from fastapi import FastAPI

from app.api import chats, messages

app = FastAPI()

# Incluir las APIs directamente
app.include_router(chats.router, prefix="/chats", tags=["Chats"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Chat API!"}
