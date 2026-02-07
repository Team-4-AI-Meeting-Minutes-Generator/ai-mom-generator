# Google Meet Integration Setup Guide

To enable automated meeting retrieval, follow these steps to set up your Google Cloud project.

## 1. Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., "Thynk Tech Meet").
3. Enable the **Google Meet API** and **Google Calendar API**.

## 2. OAuth 2.0 Credentials
1. Go to **APIs & Services > Credentials**.
2. Click **Create Credentials > OAuth client ID**.
3. Set the application type to **Desktop App** (for development).
4. Download the `credentials.json` file and place it in the `src/` directory.

## 3. Scopes Required
Your app will request the following scopes:
- `https://www.googleapis.com/auth/meetings.space.readonly`
- `https://www.googleapis.com/auth/calendar.events.readonly`

---

> [!NOTE]
> For **Live Sync** (transcribing the Meet tab while you are in it), no API setup is required. The app will capture the audio directly from your browser with your permission!
