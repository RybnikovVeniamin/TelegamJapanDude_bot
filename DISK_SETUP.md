# Setting Up Persistent Disk on Render

To prevent data loss (counter and keywords) when the bot restarts.

## Step 1: Add a disk to your service

1. Go to [render.com](https://render.com) → your bot service
2. Open the **"Disks"** tab
3. Click **"Add Disk"**
4. Fill in:
   - **Mount path**: `/var/data`
   - **Size**: `1 GB` (minimum, more than enough)
5. Click **"Add Disk"**

The bot will automatically restart.

## Step 2: Restore the counter

After restart, send this command in your chat:
```
/setcount 58
```
(replace 58 with your actual counter value)

---

## ✅ Done!

Now all data is saved on disk and won't be lost.

## Bot Commands

| Command | Description |
|---------|-------------|
| `/what` | Show tracked keywords |
| `/add word` | Add a new keyword to track |
| `/list` | List all tracked keywords |
| `/setcount 58` | Manually set the counter value |
