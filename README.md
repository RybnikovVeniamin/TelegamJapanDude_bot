# English Voice Analyzer 🎤

A simple web application that helps you improve your English speaking skills by analyzing your voice recordings.

## What It Does

This tool records your English speech and provides:
- **Speech Recognition**: Converts your voice to text
- **Grammar Analysis**: Finds repeated words, long sentences, and filler words
- **Score**: Gives you a score out of 100
- **Tips**: Provides helpful suggestions to improve your pronunciation

## How to Use

### Step 1: Install Required Software

First, you need to install Python (if you don't have it already). Then install the required packages:

```bash
pip install -r requirements.txt
```

**Note**: For audio format conversion, you may also need to install FFmpeg:
- **Mac**: `brew install ffmpeg`
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)

If you don't install FFmpeg, the app will still work, but some audio formats might not be supported.

### Step 2: Run the Application

Open your terminal, go to the project folder, and run:

```bash
python app.py
```

### Step 3: Open in Browser

Once the app is running, open your web browser and go to:

```
http://localhost:5001
```

**Note**: We use port 5001 instead of 5000 because macOS uses port 5000 for AirPlay by default.

### Step 4: Record and Analyze

1. Click the "Start Recording" button
2. Speak in English
3. Click "Stop Recording" when you're done
4. Wait for the analysis (it takes a few seconds)
5. See your results, score, and tips!

## Features

- ✅ Real-time voice recording
- ✅ Automatic speech-to-text conversion
- ✅ Grammar and pronunciation analysis
- ✅ Visual score display
- ✅ Helpful improvement tips
- ✅ Beautiful, easy-to-use interface

## Notes

- You need an internet connection (uses Google's speech recognition service)
- Make sure to allow microphone access when your browser asks
- Speak clearly for best results
- The tool works best with English (US) pronunciation

## Troubleshooting

**Problem**: "Could not understand audio"
- **Solution**: Speak louder and more clearly, make sure you're speaking in English

**Problem**: Microphone not working
- **Solution**: Check your browser settings and allow microphone access

**Problem**: Analysis takes too long
- **Solution**: Check your internet connection

Enjoy improving your English! 🚀

