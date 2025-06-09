import os
from os import environ

# Bot Configuration
API_ID = environ.get("API_ID", "25198711")
API_HASH = environ.get("API_HASH", "2a99a1375e26295626c04b4606f72752")
BOT_TOKEN = environ.get("BOT_TOKEN", "7780406992:AAH1PTSFdCiQ4ZK0QMDk9LGY4cAD-C8ZETo")

# Directory Configuration
DOWNLOAD_DIR = "downloads"
EXTRACT_DIR = "extracted"
CREDS_DIR = "credentials"

# Google Drive OAuth Configuration
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_ID = environ.get("CLIENT_ID", "87332514617-la1rp20dtt4ddg7knr6juks4urpvm28s.apps.googleusercontent.com")
CLIENT_SECRET = environ.get("CLIENT_SECRET", "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")

# Bot Profile Picture
BOT_PIC_URL = "https://iili.io/F3pawHx.jpg"

# Create directories if they don't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACT_DIR, exist_ok=True)
os.makedirs(CREDS_DIR, exist_ok=True)
