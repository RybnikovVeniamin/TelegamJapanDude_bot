# Deploy Your Bot to the Cloud ☁️

This guide will help you run your Telegram bot in the cloud so it works 24/7 without needing your computer to be on.

**⚠️ Note:** Render.com is no longer free. See `FREE_HOSTING_GUIDE.md` for current free and cheap options!

## Option 1: Railway (Recommended - Easiest & Very Cheap) 🚂

Railway is the easiest option with a free $5 credit, then about $0.50-1/month (super cheap for a hobby bot!)

### Step 1: Create a GitHub Account (if you don't have one)

1. Go to [github.com](https://github.com) and sign up (it's free)
2. Create a new account or sign in

### Step 2: Upload Your Code to GitHub

1. On GitHub, click the "+" icon in the top right
2. Click "New repository"
3. Name it something like "telegram-keyword-bot"
4. Make it **Public** (free accounts need public repos)
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

### Step 3: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account (click "Start a New Project")
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository (telegram-keyword-bot)
6. Railway will automatically detect it's a Python app!
7. Go to the "Variables" tab
8. Click "New Variable"
9. Add environment variable:
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `your-bot-token-here` (get this from @BotFather on Telegram)
10. Railway will automatically deploy!
11. Wait 1-2 minutes - you'll see "Deployed" when it's ready

### Step 4: Test It

Once it's deployed, your bot is running in the cloud! Test it in your Telegram channel - it should work exactly the same, but now it runs 24/7.

---

## Option 2: Fly.io (100% Free) 🪰

Fly.io offers a completely free tier that's perfect for small bots.

See `FREE_HOSTING_GUIDE.md` for detailed Fly.io setup instructions (requires installing a small tool first).

---

---

## Important Notes 📝

- **Railway** gives you $5 free credit to start (lasts months for a small bot), then it's about $0.50-1/month
- **Fly.io** is completely free for small bots
- Your bot token is stored securely in the cloud service's settings
- You can stop/restart your bot anytime from the cloud dashboard
- If you update your code, push to GitHub and the cloud service will automatically update
- Both Railway and Fly.io keep your bot running 24/7 (no sleeping)

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

## 💰 Cost Comparison

For more options and detailed cost comparison, see `FREE_HOSTING_GUIDE.md`

**Recommendation**: Start with **Railway** - it's the easiest and very cheap (basically free for hobby projects)! 🎯

