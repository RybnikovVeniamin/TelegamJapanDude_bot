# Deploy Your Bot to the Cloud ☁️

This guide will help you run your Telegram bot in the cloud so it works 24/7 without needing your computer to be on.

## Option 1: Render (Recommended - Easiest) 🚀

Render is a free cloud service that's perfect for beginners.

### Step 1: Create a GitHub Account (if you don't have one)

1. Go to [github.com](https://github.com) and sign up (it's free)
2. Create a new account or sign in

### Step 2: Upload Your Code to GitHub

1. On GitHub, click the "+" icon in the top right
2. Click "New repository"
3. Name it something like "telegram-keyword-bot"
4. Make it **Public** (free accounts need public repos for free hosting)
5. Click "Create repository"
6. GitHub will show you instructions, but here's the simple way:

**If you have GitHub Desktop installed:**
- Open GitHub Desktop
- Click "File" → "Add Local Repository"
- Select your project folder
- Click "Publish repository"

**Or use the terminal:**
```bash
cd /Users/veniaminrybnikov/call-analyzer
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/telegram-keyword-bot.git
git push -u origin main
```
(Replace YOUR_USERNAME with your GitHub username)

### Step 3: Deploy to Render

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account (click "Get Started for Free")
3. Click "New +" button
4. Select "Background Worker"
5. Connect your GitHub account if asked
6. Select your repository (telegram-keyword-bot)
7. Fill in the settings:
   - **Name**: telegram-keyword-bot (or any name you like)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python3 telegram_bot.py`
8. Scroll down to "Environment Variables"
9. Click "Add Environment Variable"
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `8562930250:AAEeCXhc0ivFippDdai1jejVENAx88g8s7g` (your token)
10. Click "Create Background Worker"
11. Wait 2-3 minutes for it to deploy
12. You'll see "Live" when it's ready!

### Step 4: Test It

Once it says "Live", your bot is running in the cloud! Test it in your Telegram channel - it should work exactly the same, but now it runs 24/7.

---

## Option 2: Railway (Alternative) 🚂

Railway is another easy option with a free tier.

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway will automatically detect it's a Python app
7. Go to "Variables" tab
8. Add: `TELEGRAM_BOT_TOKEN` = `8562930250:AAEeCXhc0ivFippDdai1jejVENAx88g8s7g`
9. Click "Deploy"
10. Wait for it to finish - your bot is now in the cloud!

---

## Option 3: PythonAnywhere (Simple Alternative) 🐍

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free account
3. Go to "Files" tab
4. Upload your files (telegram_bot.py, requirements.txt)
5. Go to "Tasks" tab
6. Create a new task that runs: `python3 telegram_bot.py`
7. Set it to run "Always" (every day)
8. Go to "Consoles" tab
9. Start a new console and run: `pip3.9 install --user -r requirements.txt`
10. In the console, set your token: `export TELEGRAM_BOT_TOKEN="your-token"`
11. Run: `python3 telegram_bot.py`

---

## Important Notes 📝

- **Free tiers** usually have some limitations (like the service might sleep after inactivity)
- **Render** and **Railway** free tiers are usually always-on for small bots
- Your bot token is stored securely in the cloud service's settings
- You can stop/restart your bot anytime from the cloud dashboard
- If you update your code, push to GitHub and the cloud service will automatically update

## Troubleshooting

**Bot stops working after a while:**
- Check the cloud service dashboard for any error messages
- Make sure the environment variable (TELEGRAM_BOT_TOKEN) is set correctly
- Restart the service from the dashboard

**Need to change the keyword:**
- Edit `telegram_bot.py` on your computer
- Push the changes to GitHub
- The cloud service will automatically update

---

**Recommendation**: Start with **Render** - it's the easiest for beginners! 🎯

