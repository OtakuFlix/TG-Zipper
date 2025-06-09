
---


# ✨🎒 OtakuFlix File Summoner Bot 「Aniflix Edition」

A sleek & powerful **Telegram bot** by **@Otakuflix**, created for the ultimate anime and file lovers! 🧲 This bot can **download files from direct links**, **extract them like a ninja**, and **upload them straight to your Google Drive** — with full flair, status bars, and magical buttons ✨

📢 **Join our official channel** for updates, anime uploads & magic tools: [@Aniflix_official](https://t.me/Aniflix_official)

![Bot Preview](https://iili.io/F3pawHx.jpg)

---

## 🌟 Features That’ll Make You Say "Sugoi~"

- 📥 **Multi-Format Downloads** – Fetch anything from direct links (MEGA, GDrive, etc.)
- 📂 **Auto Extraction** – Unzips ZIP, RAR, and 7Z like a true unpacking master
- ☁️ **Google Drive Upload** – Seamlessly throws files into your Drive
- 📊 **Live Progress** – Smooth animated progress bars you’ll actually love
- 🤖 **User-Friendly UI** – Clickable menus, inline buttons & clean flows
- 🔐 **Secure** – OAuth 2.0 protection keeps your Drive safe
- 🚀 **Optimized** – Fast, stable, and reliable performance for marathon use

---

## 🚀 Quick Start: Summon Your Bot in 4 Steps

### 1. 🛠️ Get a Telegram Bot Token
- Talk to [@BotFather](https://t.me/botfather)
- Create a new bot, save the token

### 2. ☁️ Google Cloud Setup
- Visit [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project, enable **Google Drive API**
- Create **OAuth 2.0 credentials** (Desktop type)
- Download the `credentials.json` file

### 3. 🧪 Setup Your Project
```bash
git clone https://github.com/Otakuflix/TG-Zipper.git
cd TG-Zipper
pip install -r requirements.txt
```

* Create your `.env` file:

```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_telegram_bot_token
CLIENT_ID=your_google_client_id
CLIENT_SECRET=your_google_client_secret
PORT=10000
PYTHONUNBUFFERED=1
```

### 4. 🎮 Run It Like a Pro

```bash
python bot.py
```

---

## 🧾 Bot Commands Cheat Sheet

| Command           | Description                          |
| ----------------- | ------------------------------------ |
| `/start`          | Activate bot and show main menu      |
| `/help`           | Full user guide and feature list     |
| `/oauth`          | Authenticate Google account          |
| `/setfolder [id]` | Set your default Google Drive folder |
| `/status`         | Check current status and usage       |

---

## 📦 Requirements

* 🐍 Python 3.8 or higher
* 🤖 Telegram Bot Token from BotFather
* ☁️ Google Cloud Project with Drive API
* ⚙️ `requirements.txt` installed

---

## 🧩 Dependencies

* `pyrogram` – Telegram API made simple
* `google-api-python-client` – GDrive upload
* `google-auth` – OAuth secure login
* `rarfile` – For RAR archive magic
* `py7zr` – Unpack 7z like a pro
* `requests` – HTTP for grabbing links

---

## 🐳 Easy Docker Deployment (Optional)

```bash
docker build -t otakuflix-bot .
docker run -d --name otakuflix-bot --env-file .env otakuflix-bot
```

---

## 🌎 Cloud Deployment (Koyeb, Railway, Render etc.)

* Use platforms like [Koyeb](https://www.koyeb.com/), [Render](https://render.com/), or [Railway](https://railway.app/)
* Point to your GitHub repo and add `.env` secrets
* Choose `python bot.py` as the run command

---

## ❤️ Made with Love by @Otakuflix

🧩 Inspired by anime, built for the community.

📢 Stay connected for updates, anime uploads, and exclusive bots:
👉 [@Aniflix\_official](https://t.me/Aniflix_official)

---

> "Power comes in response to a need, not a desire."
> – Goku 🔥

```

<div align="center">

# ✨🎒 OtakuFlix File Summoner Bot 「Aniflix Edition」

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0.106-00a8ff?style=for-the-badge&logo=telegram&logoColor=white)](https://pyrogram.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Channel](https://img.shields.io/badge/Join-@Aniflix__official-0088cc?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Aniflix_official)

*The ultimate anime file management assistant for Telegram*

![Banner](https://iili.io/F3pawHx.jpg)

<div align="center" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin: 20px 0;">
    <a href="https://app.koyeb.com/deploy?type=git&repository=github.com/yourusername/tele_extract_bot&branch=main&name=otakuflix-bot&ports=8080;http;/&env[BOT_TOKEN]&env[CLIENT_ID]&env[CLIENT_SECRET]">
        <img src="https://www.koyeb.com/static/images/deploy/button.svg" alt="Deploy on Koyeb" height="40">
    </a>
    <a href="https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2Fyourusername%2Ftele_extract_bot">
        <img src="https://railway.app/button.svg" alt="Deploy on Railway" height="40">
    </a>
    <a href="https://render.com/deploy?repo=https://github.com/yourusername/tele_extract_bot">
        <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render" height="40">
    </a>
    <a href="https://deploy.workers.cloudflare.com/?url=https://github.com/yourusername/tele_extract_bot">
        <img src="https://raw.githubusercontent.com/cloudflare/workers-devtool/main/images/deploy-button.svg" alt="Deploy to Cloudflare Workers" height="40">
    </a>
</div>

</div>

## 🌟 Features That'll Make You Say "Sugoi~"

<div align="center">

| 🎯 Feature | 💡 Description |
|------------|---------------|
| 📥 **Multi-Source Downloads** | Fetch from direct links, MEGA, GDrive, and more |
| 🧩 **Smart Extraction** | Auto-unzip ZIP, RAR, 7Z like a true unpacking master |
| ☁️ **GDrive Sync** | Seamless upload to your personal Google Drive |
| 🎨 **Anime-Themed UI** | Beautiful interface with interactive buttons |
| 📊 **Live Progress** | Real-time progress bars and status updates |
| 🔐 **Military-Grade Security** | OAuth 2.0 protected, no data leaks |
| ⚡ **Lightning Fast** | Optimized for speed and reliability |

</div>

## 🚀 Quick Start: 4-Step Deployment

### 1️⃣ Create Your Bot
- Talk to [@BotFather](https://t.me/botfather) and create a new bot
- Save your bot token (you'll need it later)

### 2️⃣ Google Cloud Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Google Drive API**
4. Configure OAuth consent screen
5. Create OAuth 2.0 credentials (Desktop app type)
6. Download `credentials.json`

### 3️⃣ Deploy (Choose One)

#### 🐍 Local Setup
```bash
git clone https://github.com/yourusername/tele_extract_bot.git
cd tele_extract_bot
pip install -r requirements.txt

# Create .env file
echo "BOT_TOKEN=your_bot_token_here" > .env
echo "CLIENT_ID=your_client_id_here" >> .env
echo "CLIENT_SECRET=your_client_secret_here" >> .env

# Run the bot
python bot.py
```

#### 🐳 Using Docker
```bash
docker build -t otakuflix-bot .
docker run -d --name otakuflix-bot --env-file .env otakuflix-bot
```

## 🚀 One-Click Deployment

<div align="center" style="margin: 1rem 0 2rem 0;">

### ☁️ Choose Your Deployment Platform

<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin: 1.5rem 0;">

<a href="https://render.com/deploy?repo=https://github.com/Otakuflix/TG-Zipper&env=API_ID=YOUR_API_ID,API_HASH=YOUR_API_HASH,BOT_TOKEN=YOUR_BOT_TOKEN,CLIENT_ID=YOUR_GOOGLE_CLIENT_ID,CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET">
  <img src="https://img.shields.io/badge/🚀_Deploy_to_Render-46E3B7?style=for-the-badge&logo=render&logoColor=white&labelColor=121212&color=46E3B7&borderColor=46E3B7&borderWidth=2px&borderRadius=12px&padding=8px" alt="Deploy to Render" style="border-radius: 12px;">
</a>

<a href="https://railway.app/template/8tQ2kO?referralCode=OtakuFlix">
  <img src="https://img.shields.io/badge/🚂_Deploy_on_Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white&labelColor=0B0D0E&color=white&borderColor=0B0D0E&borderWidth=2px&borderRadius=12px&padding=8px" alt="Deploy on Railway" style="border-radius: 12px;">
</a>

<a href="https://app.koyeb.com/deploy?type=git&repository=github.com/Otakuflix/TG-Zipper&branch=main&name=otakuflix-bot&ports=8080;http;/&env[API_ID]=YOUR_API_ID&env[API_HASH]=YOUR_API_HASH&env[BOT_TOKEN]=YOUR_BOT_TOKEN&env[CLIENT_ID]=YOUR_GOOGLE_CLIENT_ID&env[CLIENT_SECRET]=YOUR_GOOGLE_CLIENT_SECRET">
  <img src="https://img.shields.io/badge/☁️_Deploy_on_Koyeb-121212?style=for-the-badge&logo=koyeb&logoColor=white&labelColor=121212&color=white&borderColor=121212&borderWidth=2px&borderRadius=12px&padding=8px" alt="Deploy on Koyeb" style="border-radius: 12px;">
</a>

<a href="https://heroku.com/deploy?template=https://github.com/Otakuflix/TG-Zipper">
  <img src="https://img.shields.io/badge/🦸_Deploy_to_Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white&labelColor=430098&color=white&borderColor=430098&borderWidth=2px&borderRadius=12px&padding=8px" alt="Deploy to Heroku" style="border-radius: 12px;">
</a>

<a href="https://dash.cloudflare.com/?to=/:account/workers/overview">
  <img src="https://img.shields.io/badge/🌩️_Deploy_on_Cloudflare-F38020?style=for-the-badge&logo=cloudflare&logoColor=white&labelColor=F38020&color=white&borderColor=F38020&borderWidth=2px&borderRadius=12px&padding=8px" alt="Deploy on Cloudflare" style="border-radius: 12px;">
</a>

</div>

</div>

### ⚙️ Required Environment Variables

```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_telegram_bot_token
CLIENT_ID=your_google_client_id
CLIENT_SECRET=your_google_client_secret
PORT=10000  # Required for Render
PYTHONUNBUFFERED=1
```

### Required Environment Variables:

```
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_telegram_bot_token
CLIENT_ID=your_google_client_id
CLIENT_SECRET=your_google_client_secret
PORT=10000  # For Render compatibility
PYTHONUNBUFFERED=1
```

### ⚙️ Required Environment Variables
After deployment, set these in your platform's settings:

```
BOT_TOKEN=your_telegram_bot_token
CLIENT_ID=your_google_client_id
CLIENT_SECRET=your_google_client_secret
PORT=8080  # For Koyeb/Render
PYTHONUNBUFFERED=1
```

### 4️⃣ Authenticate
1. Start a chat with your bot
2. Use `/start` command
3. Click "🔐 Connect Google Drive"
4. Follow the authentication flow

## 🎮 Bot Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Start the bot | `/start` |
| `/help` | Show help menu | `/help` |
| `/oauth` | Re-authenticate Google | `/oauth` |
| `/setfolder [id]` | Set default GDrive folder | `/setfolder 1A2B3C4D` |
| `/status` | Check bot status | `/status` |

## 🛠️ Requirements

- Python 3.8+
- Telegram Bot Token
- Google Cloud Project
- Required packages in `requirements.txt`

## 🧩 Tech Stack

- **Backend**: Python 3.8+
- **Telegram API**: Pyrogram
- **Cloud Storage**: Google Drive API
- **Archive Support**: rarfile, py7zr
- **Dependencies**: See [requirements.txt](requirements.txt)

## 🌐 Deployment Options

### 🐳 Docker
```bash
docker-compose up -d
```

### ☁️ Cloud Platforms
- [Koyeb](https://www.koyeb.com/)
- [Railway](https://railway.app/)
- [Render](https://render.com/)
- [Heroku](https://heroku.com/)

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Support

- 📢 Join our channel: [@Aniflix_official](https://t.me/Aniflix_official)
- 💬 Support group: [@Aniflix_Support](https://t.me/Aniflix_Support)
- ⭐ Star this repo if you like it!

---

<div align="center">

> "Believe in the me that believes in you!"
> — Kamina, Gurren Lagann

✨ **Happy Uploading, Otaku Commander!** ✨

[![Anime Quote](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=18&pause=1000&color=FF79C6&center=true&vCenter=true&width=800&height=50&lines=Made+with+%E2%9D%A4%EF%B8%8F+by+%40Otakuflix;For+all+the+anime+enthusiasts+out+there;Power+up+your+file+management+game!)](https://github.com/yourusername/tele_extract_bot)

</div>
