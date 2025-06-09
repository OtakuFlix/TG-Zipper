from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
from bot import ModernFileDownloaderBot
import os

app = FastAPI(title="OtakuFlix Bot")
bot = None

@app.on_event("startup")
async def startup_event():
    global bot
    bot = ModernFileDownloaderBot()
    asyncio.create_task(bot.start())

@app.get("/")
async def root():
    return {"status": "OtakuFlix Bot is running!"}

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"}, status_code=200)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
