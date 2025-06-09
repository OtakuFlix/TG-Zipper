from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import os
import logging
from bot import ModernFileDownloaderBot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="OtakuFlix Bot")
bot = None

@app.on_event("startup")
async def startup_event():
    global bot
    try:
        logger.info("Initializing bot...")
        bot = ModernFileDownloaderBot()
        # Start the bot in the background
        asyncio.create_task(bot.start())
        logger.info("Bot initialization complete")
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        raise

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"status": "OtakuFlix Bot is running!"}

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    try:
        # Add more health checks here if needed
        return {"status": "healthy", "service": "running"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "error": str(e)}
        )

# Handle 404 Not Found
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"status": "error", "message": "Not Found"}
    )

# Handle 500 Internal Server Error
@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal Server Error"}
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        log_level="info",
        reload=os.getenv("ENV") == "development"
    )
