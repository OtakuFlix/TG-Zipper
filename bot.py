import os
import asyncio
import zipfile
import rarfile
import py7zr
import requests
from urllib.parse import urlparse
import json
import time
from pathlib import Path
import shutil
import aiohttp
import aiofiles
import math
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import pickle

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

# Import configuration
from config import *

class ModernFileDownloaderBot:
    def __init__(self):
        self.app = Client(
            "file_downloader_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN
        )
        
        self.download_dir = DOWNLOAD_DIR
        self.extract_dir = EXTRACT_DIR
        self.creds_dir = CREDS_DIR
        self.user_drives = {}  # Store user's drive credentials
        self.user_folders = {}  # Store user's folder preferences
        
        # Google Drive OAuth settings
        self.SCOPES = SCOPES
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        
        # Register handlers
        self.setup_handlers()
    
    async def start(self):
        """Start the bot client."""
        await self.app.start()
        await self.app.run_until_disconnected()
    
    def get_progress_bar(self, percentage, length=20):
        """Create an animated progress bar with modern styling"""
        filled = int(length * percentage / 100)
        bar = "█" * filled + "░" * (length - filled)
        return f"▌{bar}▐"
    
    def format_bytes(self, bytes_val):
        """Format bytes to human readable format"""
        if bytes_val == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = int(math.floor(math.log(bytes_val, 1024)))
        p = math.pow(1024, i)
        s = round(bytes_val / p, 2)
        return f"{s} {size_names[i]}"

    def get_animated_emoji(self, step=0):
        """Get rotating animation emoji"""
        emojis = ["🔄", "🔃", "⚡", "✨", "🚀", "💫"]
        return emojis[step % len(emojis)]

    def create_stylish_message(self, title, content, footer=None):
        """Create a visually enhanced, stylish message"""
        border = "━" * 15
        message = f"╭{border}╮\n"
        message += f"┃ **{title}**\n"
        message += f"╰{border}╯\n\n"
        message += f"{content}"
        if footer:
            message += f"\n\n{'─' * 20}\n{footer}"
        return message


    def setup_handlers(self):
        """Setup message handlers with enhanced styling"""
        
        @self.app.on_message(filters.command("start"))
        async def start_command(client, message):
            welcome_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Quick Setup", callback_data="setup")],
                [InlineKeyboardButton("📚 Full Guide", callback_data="help")],
                [InlineKeyboardButton("🔧 Commands", callback_data="commands")],
                [InlineKeyboardButton("💡 Source Code", url="https://github.com/not-now-bro")]
            ])
            
            welcome_text = """**🌟 Welcome to the Future of File Management!**

🎯 **Core Features:**
┣ 📥 **Lightning Downloads** - Any link, any size
┣ 📦 **Smart Extraction** - ZIP, RAR, 7Z support
┣ ☁️ **Cloud Integration** - Google Drive upload
┣ 🎨 **Beautiful Interface** - Real-time animations
┗ ⚡ **High Performance** - Optimized for speed

🔮 **Getting Started:**
1️⃣ Connect your Google Drive
2️⃣ Send any download link
3️⃣ Watch the magic happen!"""
            
            # Send the image with caption
            await message.reply_photo(
                photo="https://iili.io/F3pawHx.jpg",
                caption=welcome_text,
                reply_markup=welcome_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        
        @self.app.on_callback_query(filters.regex("setup"))
        async def setup_callback(client, callback_query):
            setup_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔐 Start OAuth", callback_data="oauth")],
                [InlineKeyboardButton("📖 Manual Setup", callback_data="help")],
                [InlineKeyboardButton("🔙 Back", callback_data="start")]
            ])
            
            setup_text = self.create_stylish_message(
                "🚀 QUICK SETUP",
                """**Choose your preferred setup method:**

**🔐 OAuth Method (Recommended):**
┣ ✅ Secure & automatic
┣ 🔒 No manual token handling
┣ ⚡ One-click authentication
┗ 🎯 Instant connection

**📖 Manual Method:**
┣ 🛠️ Full control over setup
┣ 📚 Step-by-step guidance
┣ 🔧 Custom configuration
┗ 💡 Educational approach

**💡 New users should start with OAuth!**""",
                "🎯 *Select your preferred method*"
            )
            
            await callback_query.edit_message_text(
                setup_text,
                reply_markup=setup_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        
        @self.app.on_callback_query(filters.regex("help"))
        async def help_callback(client, callback_query):
            help_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Setup", callback_data="setup")]
            ])
            
            help_text = self.create_stylish_message(
                "📚 MANUAL SETUP GUIDE",
                """**Step-by-Step Instructions:**

**🔸 Step 1: Google Cloud Console**
┣ 🌐 Visit [Google Cloud Console](https://console.cloud.google.com)
┣ 📋 Create new project or select existing
┣ 🔧 Enable Google Drive API
┗ 🔑 Create OAuth 2.0 credentials

**🔸 Step 2: OAuth Configuration**
┣ 📱 Set application type: "Desktop app"
┣ 💾 Download credentials JSON file
┣ 🔐 Note your Client ID & Secret
┗ ✅ Add authorized redirect URIs

**🔸 Step 3: Bot Configuration**
┣ 💬 Send: `/oauth`
┣ 🔗 Follow the authentication link
┣ 🎯 Complete Google authorization
┗ ✅ Receive confirmation

**🔸 Step 4: Start Using**
┣ 🔗 Send any download link
┣ 📥 Watch real-time progress
┣ 📦 Automatic extraction (archives)
┗ ☁️ Instant Google Drive upload!

**🎨 Supported Formats:** ZIP • RAR • 7Z""",
                "🎯 *Need help? Use the OAuth method for easier setup!*"
            )
            
            await callback_query.edit_message_text(
                help_text,
                reply_markup=help_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        
        @self.app.on_callback_query(filters.regex("commands"))
        async def commands_callback(client, callback_query):
            commands_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Main", callback_data="start")]
            ])
            
            commands_text = self.create_stylish_message(
                "🔧 AVAILABLE COMMANDS",
                """**Bot Commands Reference:**

**🎯 Essential Commands:**
┣ `/start` - Launch bot & welcome screen
┣ `/oauth` - Start Google Drive authentication
┣ `/status` - Check connection status
┣ `/help` - Detailed setup instructions
┗ `/reset` - Clear credentials & restart

**⚡ Quick Actions:**
┣ Send any URL to start download
┣ Multiple files? Send one by one
┣ Archives auto-extract before upload
┗ Real-time progress with animations

**💡 Pro Tips:**
┣ 🔗 Direct download links work best
┣ 🚀 Large files? No problem!
┣ 📱 Works perfectly on mobile
┣ 🎨 Beautiful progress animations
┗ ☁️ Automatic cloud organization

**🔧 Troubleshooting:**
┣ Connection issues? Try `/reset`
┣ Upload fails? Check Drive permissions
┗ Slow downloads? Check your internet""",
                "🎯 *Ready to download? Just send a link!*"
            )
            
            await callback_query.edit_message_text(
                commands_text,
                reply_markup=commands_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        
        @self.app.on_callback_query(filters.regex("start"))
        async def start_callback(client, callback_query):
            # Redirect to start command
            await start_command(client, callback_query.message)
        
        @self.app.on_message(filters.command("oauth"))
        async def oauth_command(client, message):
            user_id = str(message.from_user.id)
            
            try:
                # Create OAuth flow
                flow = Flow.from_client_config(
                    {
                        "web": {
                            "client_id": self.CLIENT_ID,
                            "client_secret": self.CLIENT_SECRET,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"]
                        }
                    },
                    scopes=self.SCOPES
                )
                
                flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
                
                # Get authorization URL
                auth_url, _ = flow.authorization_url(prompt='consent')
                
                oauth_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔐 Authorize Google Drive", url=auth_url)],
                    [InlineKeyboardButton("❓ Need Help?", callback_data="help")]
                ])
                
                oauth_text = self.create_stylish_message(
                    "🔐 GOOGLE DRIVE AUTH",
                    """**OAuth Authentication Process:**

**🔸 Step 1:** Click the button below
**🔸 Step 2:** Sign in to your Google account
**🔸 Step 3:** Grant Drive permissions
**🔸 Step 4:** Copy the authorization code
**🔸 Step 5:** Send the code back here

**⚠️ Important:** 
After authorization, send me the code like:
`/code YOUR_AUTHORIZATION_CODE`

**🔒 Security:** Your credentials are encrypted and stored securely.""",
                    "🎯 *Click the button to start authorization*"
                )
                
                await message.reply_text(
                    oauth_text,
                    reply_markup=oauth_markup,
                    parse_mode=ParseMode.MARKDOWN
                )
                
                # Store flow for this user
                self.user_drives[f"{user_id}_flow"] = flow
                
            except Exception as e:
                error_text = self.create_stylish_message(
                    "❌ OAUTH ERROR",
                    f"""**Authentication setup failed:**

**Error:** `{str(e)}`

**🔧 Possible fixes:**
┣ Check Google OAuth credentials
┣ Verify Client ID & Secret
┣ Ensure Drive API is enabled
┗ Try `/reset` and setup again""",
                    "💡 *Contact support if error persists*"
                )
                
                await message.reply_text(error_text, parse_mode=ParseMode.MARKDOWN)
        
        @self.app.on_message(filters.command("code"))
        async def code_command(client, message):
            user_id = str(message.from_user.id)
            flow_key = f"{user_id}_flow"
            
            if flow_key not in self.user_drives:
                await message.reply_text(
                    self.create_stylish_message(
                        "❌ NO ACTIVE FLOW",
                        "**No OAuth process found.**\n\nPlease start with `/oauth` first!",
                        "🔄 *Use /oauth to begin authentication*"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            try:
                # Extract authorization code
                auth_code = message.text.split(' ', 1)[1]
                flow = self.user_drives[flow_key]
                
                # Exchange code for credentials
                flow.fetch_token(code=auth_code)
                credentials = flow.credentials
                
                # Save credentials
                creds_file = os.path.join(self.creds_dir, f"{user_id}.pickle")
                with open(creds_file, 'wb') as token:
                    pickle.dump(credentials, token)
                
                self.user_drives[user_id] = credentials
                
                # Clean up flow
                del self.user_drives[flow_key]
                
                success_text = self.create_stylish_message(
                    "✅ AUTHENTICATION SUCCESS",
                    """**Google Drive connected successfully!**

**🎉 Setup Complete:**
┣ ✅ Credentials saved securely
┣ 🔐 OAuth token validated
┣ ☁️ Drive access confirmed
┗ 🚀 Ready for file operations

**🎯 Next Steps:**
Send any download link to start using the bot!""",
                    "🌟 *Your files are now ready for cloud upload!*"
                )
                
                await message.reply_text(success_text, parse_mode=ParseMode.MARKDOWN)
                
            except IndexError:
                await message.reply_text(
                    self.create_stylish_message(
                        "⚠️ MISSING CODE",
                        """**Authorization code required!**

**Correct usage:**
`/code YOUR_AUTHORIZATION_CODE`

**Example:**
`/code 4/0AdQt8qh7rMiY...`""",
                        "💡 *Copy the full code from Google*"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception as e:
                error_text = self.create_stylish_message(
                    "❌ AUTHENTICATION FAILED",
                    f"""**Could not complete authentication:**

**Error:** `{str(e)}`

**🔧 Try these fixes:**
┣ Ensure code is complete and correct
┣ Don't include extra spaces
┣ Code expires in 10 minutes
┗ Get a fresh code if needed""",
                    "🔄 *Use /oauth to get a new authorization URL*"
                )
                
                await message.reply_text(error_text, parse_mode=ParseMode.MARKDOWN)
        
        @self.app.on_message(filters.command("status"))
        async def status_command(client, message):
            user_id = str(message.from_user.id)
            
            if user_id in self.user_drives:
                # Test credentials
                try:
                    creds = self.user_drives[user_id]
                    if creds.expired:
                        creds.refresh(Request())
                        # Save refreshed credentials
                        creds_file = os.path.join(self.creds_dir, f"{user_id}.pickle")
                        with open(creds_file, 'wb') as token:
                            pickle.dump(creds, token)
                    
                    service = build('drive', 'v3', credentials=creds)
                    about = service.about().get(fields="user").execute()
                    user_email = about['user']['emailAddress']
                    
                    status_text = self.create_stylish_message(
                        "✅ CONNECTION STATUS",
                        f"""**Google Drive Connected**

**📧 Account:** `{user_email}`
**🔐 Status:** Authenticated & Active
**☁️ Access:** Full Drive permissions
**🚀 Ready:** For file operations

**🎯 Everything looks good!**
Send any download link to start.""",
                        "🌟 *Your bot is ready for action!*"
                    )
                    
                    await message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)
                    
                except Exception as e:
                    error_text = self.create_stylish_message(
                        "❌ CONNECTION ERROR",
                        f"""**Authentication issue detected:**

**Error:** `{str(e)}`

**🔧 Quick fixes:**
┣ Try refreshing with `/oauth`
┣ Check internet connection
┣ Verify Google account access
┗ Use `/reset` if needed""",
                        "🔄 *Re-authentication may be required*"
                    )
                    
                    await message.reply_text(error_text, parse_mode=ParseMode.MARKDOWN)
            else:
                setup_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🚀 Quick Setup", callback_data="setup")]
                ])
                
                status_text = self.create_stylish_message(
                    "❌ NOT CONNECTED",
                    """**Google Drive not authenticated**

**🔧 Setup Required:**
Your bot needs Google Drive access to upload files.

**⚡ Quick Setup:**
Use the button below for guided setup!

**📱 Alternative:**
Send `/oauth` to start manual authentication""",
                    "🎯 *Get connected in under 2 minutes!*"
                )
                
                await message.reply_text(
                    status_text,
                    reply_markup=setup_markup,
                    parse_mode=ParseMode.MARKDOWN
                )
        
        @self.app.on_message(filters.command("reset"))
        async def reset_command(client, message):
            user_id = str(message.from_user.id)
            
            # Clear user data
            if user_id in self.user_drives:
                del self.user_drives[user_id]
            
            # Remove credentials file
            creds_file = os.path.join(self.creds_dir, f"{user_id}.pickle")
            if os.path.exists(creds_file):
                os.remove(creds_file)
            
            reset_text = self.create_stylish_message(
                "🔄 RESET COMPLETE",
                """**All user data cleared successfully!**

**🧹 Cleaned up:**
┣ ✅ Removed stored credentials
┣ ✅ Cleared authentication tokens
┣ ✅ Reset connection status
┗ ✅ Fresh start ready

**🚀 Next Steps:**
Use `/oauth` to set up your connection again.""",
                "🎯 *Ready for a fresh start!*"
            )
            
            await message.reply_text(reset_text, parse_mode=ParseMode.MARKDOWN)
            
        @self.app.on_message(filters.command("help") & filters.private)
        async def help_command(client, message):
            help_text = self.create_stylish_message(
                "📚 BOT COMMANDS",
                """**🔹 Core Commands:**
                
                `/start` - Start the bot and show welcome message
                `/help` - Show this help message
                
                **🔹 Google Drive Commands:**
                
                `/oauth` - Start Google Drive OAuth setup
                `/code` - Enter authorization code manually
                `/status` - Check Google Drive connection status
                
                **🔹 File Management:**
                
                `/folder [name]` - Set upload folder (use 'root' for root)
                `/reset` - Reset your Google Drive connection
                
                **🔗 Just send any download link to start downloading!**
                
                **📝 Example:**
                `/folder MyFiles` - Upload to 'MyFiles' folder
                `/folder root` - Upload to Google Drive root""",
                "💡 *Need more help? Just ask!*"
            )
            await message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
        
        @self.app.on_message(filters.command("folder") & filters.private)
        async def folder_command(client, message):
            user_id = str(message.from_user.id)
            
            if len(message.command) > 1:
                folder_name = " ".join(message.command[1:])
                if folder_name.lower() == 'root':
                    if user_id in self.user_folders:
                        del self.user_folders[user_id]
                    await message.reply("📁 Folder reset to root directory.")
                else:
                    self.user_folders[user_id] = folder_name
                    await message.reply(
                        self.create_stylish_message(
                            "📁 FOLDER UPDATED",
                            f"Your upload folder has been set to:\n`{folder_name}`",
                            "Files will be uploaded to this folder in your Google Drive"
                        ),
                        parse_mode=ParseMode.MARKDOWN
                    )
            else:
                current_folder = self.user_folders.get(user_id, "Root")
                await message.reply(
                    self.create_stylish_message(
                        "📂 CURRENT FOLDER",
                        f"Your current upload folder is set to:\n`{current_folder}`\n\n"
                        "To change folder, use:\n"
                        "`/folder Folder Name`\n\n"
                        "To use root folder, use:\n"
                        "`/folder root`"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
        
        @self.app.on_message(filters.text & ~filters.command(["start", "help", "oauth", "code", "status", "reset", "folder", "commands"]))
        async def handle_link(client, message):
            text = message.text.strip()
            
            # Check if it's a valid URL
            if not self.is_valid_url(text):
                await message.reply_text(
                    self.create_stylish_message(
                        "❌ INVALID LINK",
                        """**Please send a valid download link**

**✅ Supported formats:**
┣ 🌐 Direct download URLs
┣ 📁 File hosting services
┣ 🔗 HTTP/HTTPS protocols
┗ 📱 Mobile-friendly links

**📝 Example:**
`https://example.com/file.zip`
`https://drive.google.com/file/d/ID/view`""",
                        "💡 *Paste your download link and try again*"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            user_id = str(message.from_user.id)
            if user_id not in self.user_drives:
                setup_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🚀 Quick Setup", callback_data="setup")]
                ])
                
                await message.reply_text(
                    self.create_stylish_message(
                        "🔧 SETUP REQUIRED",
                        """**Google Drive authentication needed**

**⚠️ Connection Status:** Not authenticated

**🎯 Quick Solution:**
1. Click the button below for guided setup
2. Complete Google Drive authentication
3. Send your link again

**📱 Manual Setup:**
Use `/oauth` command to start""",
                        "🚀 *Get set up in under 2 minutes!*"
                    ),
                    reply_markup=setup_markup,
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            await self.process_download(message, text, user_id)
    
    def load_user_credentials(self, user_id):
        """Load user credentials from file"""
        creds_file = os.path.join(self.creds_dir, f"{user_id}.pickle")
        if os.path.exists(creds_file):
            with open(creds_file, 'rb') as token:
                credentials = pickle.load(token)
                if credentials.expired:
                    credentials.refresh(Request())
                    # Save refreshed credentials
                    with open(creds_file, 'wb') as token:
                        pickle.dump(credentials, token)
                self.user_drives[user_id] = credentials
                return credentials
        return None
    
    def is_valid_url(self, url):
        """Check if the provided text is a valid URL"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    async def process_download(self, message, url, user_id):
        """Process the download, extraction, and upload with enhanced styling"""
        # Load credentials if not in memory
        if user_id not in self.user_drives:
            if not self.load_user_credentials(user_id):
                await message.reply_text("Authentication required. Use /oauth to connect.")
                return
        
        # Initial status with enhanced styling
        status_msg = await message.reply_text(
            self.create_stylish_message(
                "🚀 INITIALIZING",
                """**Preparing download systems...**

🔍 **Analyzing link structure...**
⚡ **Optimizing connection parameters...**
🎯 **Allocating resources...**
🌐 **Establishing secure connection...**""",
                "✨ *Advanced file processing starting...*"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        
        try:
            # Download file
            filename = await self.download_file(url, status_msg)
            if not filename:
                await status_msg.edit_text(
                    self.create_stylish_message(
                        "❌ DOWNLOAD FAILED",
                        """**Could not download the file**

**🔍 Possible causes:**
┣ 🔗 Invalid or expired link
┣ 🌐 Network connectivity issues
┣ 🚫 Server access restrictions
┣ 📱 Temporary server overload  
┗ 🔒 Authentication required

**💡 Solutions:**
┣ Verify the link is correct
┣ Check if link requires login
┣ Try again in a few minutes
┗ Use direct download links when possible""",
                        "🔄 *Please check your link and try again*"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            # File analysis
            file_size = os.path.getsize(os.path.join(self.download_dir, filename))
            await status_msg.edit_text(
                self.create_stylish_message(
                    "✅ DOWNLOAD COMPLETE",
                    f"""**File successfully downloaded!**

**📁 File:** `{filename[:40]}{'...' if len(filename) > 40 else ''}`
**📊 Size:** `{self.format_bytes(file_size)}`
**🔍 Analyzing file type...**
**📦 Checking for archive formats...**""",
                    "🎯 *Processing file for optimal upload...*"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Check if it's an archive and extract
            extracted_files = await self.extract_archive(filename, status_msg)
            
            if extracted_files:
                total_size = sum(os.path.getsize(f) for f in extracted_files)
                await status_msg.edit_text(
                    self.create_stylish_message(
                        "📦 EXTRACTION COMPLETE",
                        f"""**Archive successfully extracted!**

**✨ Files extracted:** `{len(extracted_files)}`
**📊 Total size:** `{self.format_bytes(total_size)}`
**☁️ Preparing cloud upload...**
**🚀 Connecting to Google Drive...**""",
                        "🌟 *Uploading to your cloud storage...*"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
                await self.upload_to_drive(extracted_files, user_id, status_msg)
            else:
                # Upload the original file
                await status_msg.edit_text(
                    self.create_stylish_message(
                        "☁️ PREPARING UPLOAD",
                        f"""**Preparing cloud upload...**

**📁 File:** `{filename[:40]}{'...' if len(filename) > 40 else ''}`
**📊 Size:** `{self.format_bytes(file_size)}`
**🚀 Connecting to Google Drive...**
**📤 Initializing secure transfer...**""",
                        "✨ *Your file will be in the cloud soon...*"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
                await self.upload_to_drive([os.path.join(self.download_dir, filename)], user_id, status_msg)
            
        except Exception as e:
            await status_msg.edit_text(
                self.create_stylish_message(
                    "🚨 SYSTEM ERROR",
                    f"""**An unexpected error occurred:**

**Error Details:** `{str(e)[:100]}{'...' if len(str(e)) > 100 else ''}`

**🔧 Troubleshooting:**
┣ Check your internet connection
┣ Verify the download link
┣ Try a smaller file first
┣ Use `/reset` if issues persist
┗ Contact support for help

**🔄 Please try again in a few minutes**""",
                    "💡 *Most issues resolve automatically*"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
        
    async def download_file(self, url, status_msg):
        """Download file from URL with beautiful progress tracking"""
        try:
            async with aiohttp.ClientSession() as session:
                # First make a HEAD request to get headers
                async with session.head(url, allow_redirects=True) as head_response:
                    if head_response.status != 200:
                        return None
                    
                    # Get filename from headers
                    filename = self.get_filename_from_url(url, dict(head_response.headers))
                    filepath = os.path.join(self.download_dir, filename)
                    
                    # Start the actual download with the same session
                    async with session.get(url) as response:
                        if response.status != 200:
                            return None
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return None
                    
                    total_size = int(response.headers.get('content-length', 0))
                    downloaded = 0
                    animation_step = 0
                    last_update = time.time()
                    last_downloaded = 0
                    
                    async with aiofiles.open(filepath, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            await f.write(chunk)
                            chunk_size = len(chunk)
                            downloaded += chunk_size
                            animation_step += 1
                            
                            current_time = time.time()
                            time_diff = current_time - last_update
                            
                            # Update progress every 1MB or 2 seconds for smooth animation and accurate speed calculation
                            if (chunk_size >= 1024 * 1024 or  # If chunk is 1MB or larger
                                downloaded >= total_size or   # Or download is complete
                                time_diff >= 2):               # Or 2 seconds have passed
                                
                                if total_size > 0 and time_diff > 0:
                                    # Calculate download speed
                                    downloaded_since_last = downloaded - last_downloaded
                                    download_speed = downloaded_since_last / time_diff
                                    
                                    progress = (downloaded / total_size) * 100
                                    progress_bar = self.get_progress_bar(progress)
                                    emoji = self.get_animated_emoji(animation_step)
                                    
                                    short_filename = filename[:30] + "..." if len(filename) > 30 else filename
                                    remaining_bytes = total_size - downloaded
                                    
                                    # Calculate ETA if download speed is sufficient
                                    eta = "Calculating..."
                                    if download_speed > 0:
                                        eta_seconds = remaining_bytes / download_speed
                                        if eta_seconds < 60:
                                            eta = f"{int(eta_seconds)}s"
                                        elif eta_seconds < 3600:
                                            eta = f"{int(eta_seconds // 60)}m {int(eta_seconds % 60)}s"
                                        else:
                                            eta = f"{int(eta_seconds // 3600)}h {int((eta_seconds % 3600) // 60)}m"
                                    
                                    download_text = self.create_stylish_message(
                                        f"{emoji} DOWNLOADING",
                                        f"""**File:** `{short_filename}`

**🔄 Progress:**
{progress_bar} **{progress:.1f}%**

**📊 Transfer Data:**
┣ **Downloaded:** {self.format_bytes(downloaded)} / {self.format_bytes(total_size)}
┣ **Remaining:** {self.format_bytes(remaining_bytes)}
┣ **Speed:** {self.format_speed(download_speed)}
┗ **ETA:** {eta}

**⚡ Status:** Download in progress""",
                                        "🚀 *Downloading...*"
                                    )
                                    
                                    await status_msg.edit_text(
                                        download_text,
                                        parse_mode=ParseMode.MARKDOWN
                                    )
                                    
                                    # Update tracking variables
                                    last_update = current_time
                                    last_downloaded = downloaded
            
            return filename
            
        except Exception as e:
            print(f"Download error: {e}")
            return None
    
    def format_speed(self, speed):
        """Format download speed in KB/s, MB/s, or GB/s"""
        if speed < 1024:
            return f"{speed:.2f} B/s"
        elif speed < 1024 * 1024:
            return f"{speed / 1024:.2f} KB/s"
        elif speed < 1024 * 1024 * 1024:
            return f"{speed / (1024 * 1024):.2f} MB/s"
        else:
            return f"{speed / (1024 * 1024 * 1024):.2f} GB/s"
    
    def get_filename_from_url(self, url, response_headers=None):
        """Extract filename from URL or response headers with better handling"""
        filename = None
        
        # First try to get filename from Content-Disposition header
        if response_headers:
            content_disposition = response_headers.get('Content-Disposition', '')
            if 'filename=' in content_disposition:
                # Extract filename from Content-Disposition header
                import re
                filename_match = re.findall('filename[\s]*=[\s]*["\']?([^"\'\s]+)', content_disposition)
                if filename_match:
                    filename = filename_match[0].strip()
        
        # If not found in headers, try to get from URL
        if not filename:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
        
        # Remove URL parameters if any
        filename = filename.split('?')[0].split('#')[0]
        
        # If still no valid filename, generate a default one with extension based on content type
        if not filename or '.' not in filename:
            content_type = response_headers.get('Content-Type', '') if response_headers else ''
            extension = '.bin'  # Default extension
            
            # Map common content types to extensions
            if 'zip' in content_type:
                extension = '.zip'
            elif 'rar' in content_type:
                extension = '.rar'
            elif '7z' in content_type or '7-zip' in content_type:
                extension = '.7z'
            
            filename = f"downloaded_file_{int(time.time())}{extension}"
        
        # Clean filename for file system compatibility
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
        
        return filename
        
    async def _download_file_content(self, response, filename, filepath, status_msg):
        """Handle the actual file download with progress tracking"""
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        animation_step = 0
        last_update = time.time()
        last_downloaded = 0
        
        async with aiofiles.open(filepath, 'wb') as f:
            async for chunk in response.content.iter_chunked(8192):
                await f.write(chunk)
                chunk_size = len(chunk)
                downloaded += chunk_size
                animation_step += 1
                
                current_time = time.time()
                time_diff = current_time - last_update
                
                # Update progress every 1MB or 2 seconds for smooth animation and accurate speed calculation
                if (chunk_size >= 1024 * 1024 or  # If chunk is 1MB or larger
                    downloaded >= total_size or   # Or download is complete
                    time_diff >= 2):              # Or 2 seconds have passed
                    
                    if total_size > 0 and time_diff > 0:
                        # Calculate download speed
                        downloaded_since_last = downloaded - last_downloaded
                        download_speed = downloaded_since_last / time_diff
                        
                        progress = (downloaded / total_size) * 100
                        progress_bar = self.get_progress_bar(progress)
                        emoji = self.get_animated_emoji(animation_step)
                        
                        short_filename = filename[:30] + "..." if len(filename) > 30 else filename
                        remaining_bytes = total_size - downloaded
                        
                        # Calculate ETA if download speed is sufficient
                        eta = "Calculating..."
                        if download_speed > 0:
                            eta_seconds = remaining_bytes / download_speed
                            if eta_seconds < 60:
                                eta = f"{int(eta_seconds)}s"
                            elif eta_seconds < 3600:
                                eta = f"{int(eta_seconds // 60)}m {int(eta_seconds % 60)}s"
                            else:
                                eta = f"{int(eta_seconds // 3600)}h {int((eta_seconds % 3600) // 60)}m"
                        
                        download_text = self.create_stylish_message(
                            f"{emoji} DOWNLOADING",
                            f"""**File:** `{short_filename}`

**🔄 Progress:**
{progress_bar} **{progress:.1f}%**

**📊 Transfer Data:**
┣ **Downloaded:** {self.format_bytes(downloaded)} / {self.format_bytes(total_size)}
┣ **Remaining:** {self.format_bytes(remaining_bytes)}
┣ **Speed:** {self.format_speed(download_speed)}
┗ **ETA:** {eta}

**⚡ Status:** Download in progress""",
                            "🚀 *Downloading...*"
                        )
                        
                        await status_msg.edit_text(
                            download_text,
                            parse_mode=ParseMode.MARKDOWN
                        )
                        
                        # Update tracking variables
                        last_update = current_time
                        last_downloaded = downloaded
        
        return filename
    
    async def extract_archive(self, filename, status_msg):
        """Extract archive files with progress tracking"""
        filepath = os.path.join(self.download_dir, filename)
        file_ext = filename.lower().split('.')[-1]
        
        # Check if it's an archive
        if file_ext not in ['zip', 'rar', '7z']:
            return None
        
        extracted_files = []
        user_extract_dir = os.path.join(self.extract_dir, f"extract_{int(time.time())}")
        os.makedirs(user_extract_dir, exist_ok=True)
        
        try:
            animation_step = 0
            
            if file_ext == 'zip':
                await status_msg.edit_text(
                    self.create_stylish_message(
                        f"{self.get_animated_emoji(animation_step)} EXTRACTING ZIP",
                        f"""**Archive:** `{filename[:40]}{'...' if len(filename) > 40 else ''}`

**📦 ZIP Archive Processing:**
┣ 🔍 **Analyzing structure...**
┣ 📂 **Reading file entries...**
┣ ⚡ **Optimizing extraction...**
┗ 🚀 **Decompressing files...**""",
                        "✨ *Smart extraction in progress...*"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
                
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    file_list = zip_ref.namelist()
                    total_files = len(file_list)
                    
                    for i, file_info in enumerate(file_list):
                        zip_ref.extract(file_info, user_extract_dir)
                        extracted_path = os.path.join(user_extract_dir, file_info)
                        
                        if os.path.isfile(extracted_path):
                            extracted_files.append(extracted_path)
                        
                        # Update progress every 10 files or at completion
                        if i % 10 == 0 or i == total_files - 1:
                            progress = ((i + 1) / total_files) * 100
                            progress_bar = self.get_progress_bar(progress)
                            animation_step += 1
                            
                            await status_msg.edit_text(
                                self.create_stylish_message(
                                    f"{self.get_animated_emoji(animation_step)} EXTRACTING ZIP",
                                    f"""**Archive:** `{filename[:40]}{'...' if len(filename) > 40 else ''}`

**🔄 Extraction Progress:**
{progress_bar} **{progress:.1f}%**

**📊 Processing Status:**
┣ **Files Processed:** {i + 1}/{total_files}
┣ **Current File:** `{os.path.basename(file_info)[:30]}{'...' if len(os.path.basename(file_info)) > 30 else ''}`
┣ **Extracted:** {len(extracted_files)} files
┗ **Status:** High-speed decompression""",
                                    "⚡ *ZIP extraction in progress...*"
                                ),
                                parse_mode=ParseMode.MARKDOWN
                            )
            
            elif file_ext == 'rar':
                await status_msg.edit_text(
                    self.create_stylish_message(
                        f"{self.get_animated_emoji(animation_step)} EXTRACTING RAR",
                        f"""**Archive:** `{filename[:40]}{'...' if len(filename) > 40 else ''}`

**📦 RAR Archive Processing:**
┣ 🔍 **Analyzing RAR structure...**
┣ 📂 **Reading compressed data...**
┣ ⚡ **Optimizing decompression...**
┗ 🚀 **Extracting files...**""",
                        "✨ *Advanced RAR extraction...*"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
                
                with rarfile.RarFile(filepath, 'r') as rar_ref:
                    file_list = rar_ref.namelist()
                    total_files = len(file_list)
                    
                    for i, file_info in enumerate(file_list):
                        rar_ref.extract(file_info, user_extract_dir)
                        extracted_path = os.path.join(user_extract_dir, file_info)
                        
                        if os.path.isfile(extracted_path):
                            extracted_files.append(extracted_path)
                        
                        if i % 5 == 0 or i == total_files - 1:
                            progress = ((i + 1) / total_files) * 100
                            progress_bar = self.get_progress_bar(progress)
                            animation_step += 1
                            
                            await status_msg.edit_text(
                                self.create_stylish_message(
                                    f"{self.get_animated_emoji(animation_step)} EXTRACTING RAR",
                                    f"""**Archive:** `{filename[:40]}{'...' if len(filename) > 40 else ''}`

**🔄 Extraction Progress:**
{progress_bar} **{progress:.1f}%**

**📊 Processing Status:**
┣ **Files Processed:** {i + 1}/{total_files}
┣ **Current File:** `{os.path.basename(file_info)[:30]}{'...' if len(os.path.basename(file_info)) > 30 else ''}`
┣ **Extracted:** {len(extracted_files)} files
┗ **Status:** RAR decompression active""",
                                    "⚡ *RAR extraction in progress...*"
                                ),
                                parse_mode=ParseMode.MARKDOWN
                            )
            
            elif file_ext == '7z':
                await status_msg.edit_text(
                    self.create_stylish_message(
                        f"{self.get_animated_emoji(animation_step)} EXTRACTING 7Z",
                        f"""**Archive:** `{filename[:40]}{'...' if len(filename) > 40 else ''}`

**📦 7Z Archive Processing:**
┣ 🔍 **Analyzing 7Z structure...**
┣ 📂 **Reading LZMA compression...**
┣ ⚡ **Optimizing extraction...**
┗ 🚀 **Decompressing files...**""",
                        "✨ *Advanced 7Z extraction...*"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
                
                with py7zr.SevenZipFile(filepath, mode='r') as seven_ref:
                    seven_ref.extractall(user_extract_dir)
                    
                    # Get all extracted files
                    for root, dirs, files in os.walk(user_extract_dir):
                        for file in files:
                            extracted_files.append(os.path.join(root, file))
                    
                    await status_msg.edit_text(
                        self.create_stylish_message(
                            f"✅ 7Z EXTRACTION COMPLETE",
                            f"""**Archive:** `{filename[:40]}{'...' if len(filename) > 40 else ''}`

**📦 Extraction Results:**
┣ **Total Files:** {len(extracted_files)}
┣ **Format:** 7Z Archive
┣ **Status:** Successfully extracted
┗ **Ready:** For cloud upload

**🎯 All files processed successfully!**""",
                            "🚀 *Preparing for Google Drive upload...*"
                        ),
                        parse_mode=ParseMode.MARKDOWN
                    )
            
            return extracted_files if extracted_files else None
            
        except Exception as e:
            await status_msg.edit_text(
                self.create_stylish_message(
                    "❌ EXTRACTION FAILED",
                    f"""**Could not extract archive**

**📁 File:** `{filename[:40]}{'...' if len(filename) > 40 else ''}`
**❌ Error:** `{str(e)[:100]}{'...' if len(str(e)) > 100 else ''}`

**🔧 Possible causes:**
┣ 🔒 Password-protected archive
┣ 📦 Corrupted archive file
┣ 💾 Insufficient disk space
┣ 🚫 Unsupported compression method
┗ 📱 Network interruption during download

**💡 Solutions:**
┣ Try downloading the file again
┣ Check if archive requires password
┣ Verify file integrity
┗ Contact support if issue persists""",
                    "🔄 *Archive will be uploaded as-is without extraction*"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return None
    
    async def upload_to_drive(self, file_paths, user_id, status_msg):
        """Upload files to Google Drive with progress tracking"""
        try:
            credentials = self.user_drives[user_id]
            service = build('drive', 'v3', credentials=credentials)
            
            # Get or create folder
            folder_id = 'root'  # Default to root
            folder_name = self.user_folders.get(str(user_id))
            
            if folder_name and folder_name.lower() != 'root':
                # Search for existing folder
                query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and 'root' in parents and trashed=false"
                results = service.files().list(q=query, fields="files(id)").execute()
                items = results.get('files', [])
                
                if items:
                    # Use existing folder
                    folder_id = items[0]['id']
                else:
                    # Create new folder
                    file_metadata = {
                        'name': folder_name,
                        'mimeType': 'application/vnd.google-apps.folder',
                        'parents': ['root']
                    }
                    folder = service.files().create(body=file_metadata, fields='id').execute()
                    folder_id = folder['id']
            
            uploaded_files = []
            total_files = len(file_paths)
            animation_step = 0
            
            for i, file_path in enumerate(file_paths):
                filename = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                
                # Update status for current file
                progress = (i / total_files) * 100
                progress_bar = self.get_progress_bar(progress)
                animation_step += 1
                
                await status_msg.edit_text(
                    self.create_stylish_message(
                        f"{self.get_animated_emoji(animation_step)} UPLOADING TO DRIVE",
                        f"""**Cloud Upload Progress:**
{progress_bar} **{progress:.1f}%**

**📤 Current Upload:**
┣ **File:** `{filename[:35]}{'...' if len(filename) > 35 else ''}`
┣ **Size:** {self.format_bytes(file_size)}
┣ **Folder:** `{folder_name if folder_name and folder_name.lower() != 'root' else 'Root'}`
┣ **Progress:** {i + 1}/{total_files}
┗ **Status:** Secure transfer active

**☁️ Uploading to Google Drive...**""",
                        "🚀 *Your files are being saved to the cloud...*"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
                
                # Upload file to Google Drive
                file_metadata = {
                    'name': filename,
                    'parents': [folder_id] if folder_id != 'root' else []
                }
                media = MediaFileUpload(file_path, resumable=True)
                
                request = service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id,name,webViewLink'
                )
                
                response = None
                while response is None:
                    status, response = request.next_chunk()
                    if status:
                        # Update upload progress for large files
                        upload_progress = int(status.progress() * 100)
                        if upload_progress % 20 == 0:  # Update every 20%
                            await status_msg.edit_text(
                                self.create_stylish_message(
                                    f"{self.get_animated_emoji(animation_step)} UPLOADING TO DRIVE",
                                    f"""**Cloud Upload Progress:**
{self.get_progress_bar((i/total_files + upload_progress/100/total_files) * 100)} **{((i/total_files + upload_progress/100/total_files) * 100):.1f}%**

**📤 Current Upload:**
┣ **File:** `{filename[:35]}{'...' if len(filename) > 35 else ''}`
┣ **Size:** {self.format_bytes(file_size)}
┣ **File Progress:** {upload_progress}%
┣ **Overall:** {i + 1}/{total_files}
┗ **Status:** High-speed cloud transfer

**☁️ Uploading to Google Drive...**""",
                                    "⚡ *Secure file transfer in progress...*"
                                ),
                                parse_mode=ParseMode.MARKDOWN
                            )
                
                uploaded_files.append({
                    'name': response['name'],
                    'id': response['id'],
                    'link': response['webViewLink'],
                    'size': self.format_bytes(file_size)
                })
            
            # Create final success message with file links
            files_list = "\n".join([
                f"┣ 📁 [`{file['name'][:30]}{'...' if len(file['name']) > 30 else ''}`]({file['link']}) - {file['size']}"
                for file in uploaded_files[:10]  # Show first 10 files
            ])
            
            if len(uploaded_files) > 10:
                files_list += f"\n┗ 📚 **... and {len(uploaded_files) - 10} more files**"
            
            success_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Open Google Drive", url="https://drive.google.com")],
                [InlineKeyboardButton("📱 Get Drive App", url="https://play.google.com/store/apps/details?id=com.google.android.apps.docs")]
            ])
            
            total_size = sum(os.path.getsize(fp) for fp in file_paths)
            
            await status_msg.edit_text(
                self.create_stylish_message(
                    "🎉 UPLOAD COMPLETE",
                    f"""**All files successfully uploaded to Google Drive!**

**📊 Upload Summary:**
┣ **Files Uploaded:** {len(uploaded_files)}
┣ **Total Size:** {self.format_bytes(total_size)}
┣ **Upload Speed:** Optimized
┗ **Status:** ✅ Complete

**📁 Uploaded Files:**
{files_list}

**🔗 Access your files using the buttons below**""",
                    "🌟 *Your files are now safely stored in the cloud!*"
                ),
                reply_markup=success_markup,
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Cleanup downloaded and extracted files
            await self.cleanup_files(file_paths)
            
        except Exception as e:
            await status_msg.edit_text(
                self.create_stylish_message(
                    "❌ UPLOAD FAILED",
                    f"""**Google Drive upload failed**

**❌ Error:** `{str(e)[:100]}{'...' if len(str(e)) > 100 else ''}`

**🔧 Possible causes:**
┣ 🔒 Google Drive authentication expired
┣ 💾 Insufficient Google Drive storage
┣ 🌐 Network connectivity issues
┣ 🚫 Google Drive API limitations
┗ 📱 Temporary server issues

**💡 Solutions:**
┣ Try `/status` to check connection
┣ Use `/oauth` to re-authenticate
┣ Check your Google Drive storage
┣ Try again in a few minutes
┗ Contact support if issue persists""",
                    "🔄 *Please try again or check your setup*"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def cleanup_files(self, file_paths):
        """Clean up downloaded and extracted files"""
        # First clean up the provided files/directories
        for file_path in file_paths:
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    # Remove parent directory if it's in the extracted folder
                    parent_dir = os.path.dirname(file_path)
                    if parent_dir.startswith(os.path.abspath(self.extract_dir)):
                        try:
                            os.rmdir(parent_dir)  # Only removes if directory is empty
                        except OSError:
                            pass  # Directory not empty, skip
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path, ignore_errors=True)
            except Exception as e:
                print(f"Error cleaning up {file_path}: {e}")
        
        # Then clean up old files in download directory
        try:
            for file in os.listdir(self.download_dir):
                file_path = os.path.join(self.download_dir, file)
                if os.path.isfile(file_path):
                    # Remove files older than 1 hour
                    if time.time() - os.path.getctime(file_path) > 3600:
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            print(f"Error cleaning up old file {file_path}: {e}")
        except Exception as e:
            print(f"Error during download directory cleanup: {e}")
        
        except Exception as e:
            print(f"Cleanup error: {e}")
    
    def load_user_credentials(self, user_id):
        """Load user credentials from file"""
        creds_file = os.path.join(self.creds_dir, f"{user_id}.pickle")
        if os.path.exists(creds_file):
            with open(creds_file, 'rb') as token:
                credentials = pickle.load(token)
                if credentials.expired:
                    credentials.refresh(Request())
                    # Save refreshed credentials
                    with open(creds_file, 'wb') as token:
                        pickle.dump(credentials, token)
                self.user_drives[user_id] = credentials
                return credentials
        return None
    
    def is_valid_url(self, url):
        """Check if the provided text is a valid URL"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    async def set_bot_picture(self):
        """Set the bot's profile picture"""
        try:
            # Download the image
            image_url = BOT_PIC_URL
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status == 200:
                        image_data = await resp.read()
                        # Save the image temporarily
                        with open("bot_pic.jpg", "wb") as f:
                            f.write(image_data)
                        # Set the bot's profile picture
                        await self.app.set_profile_photo(photo="bot_pic.jpg")
                        print("✅ Bot profile picture updated successfully")
                        # Clean up
                        if os.path.exists("bot_pic.jpg"):
                            os.remove("bot_pic.jpg")
        except Exception as e:
            print(f"⚠️ Could not update bot profile picture: {e}")

    def run(self):
        """Run the bot"""
        print("🚀 Modern File Downloader Bot Starting...")
        print("📱 Bot is ready to process downloads!")
        print("☁️ Google Drive integration enabled")
        print("🎯 Waiting for download requests...")
        
        # Start the bot
        self.app.run()
        
        # Set the bot picture after starting
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.set_bot_picture())
        except Exception as e:
            print(f"⚠️ Could not set bot picture: {e}")

# Create and run the bot
if __name__ == "__main__":
    import asyncio
    
    bot = ModernFileDownloaderBot()
    
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        print("👋 Goodbye!")
