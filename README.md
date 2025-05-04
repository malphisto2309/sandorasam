# Telegram Bot: OnlyFansFile Forwarder

This bot listens to messages from [@OnlyFansFile](https://t.me/OnlyFansFile), filters out unnecessary lines, bypasses Linkvertise, extracts the final `mega.nz` link from a `pastelink.net` page, creates a new Pastelink using your API, shortens it using GPLinks, and forwards the cleaned message with photo to your channel.

## Features

- Keeps only the message's photo and final download link.
- Bypasses the original URL using `linkvertise-bypasser`.
- Extracts only the `mega.nz` link from a Pastelink page.
- Replaces `t.me` links with `https://t.me/fansdeposit`.
- Creates a new Pastelink page with cleaned content.
- Shortens it with GPLinks and posts it to your channel.

## Your Channel

- Target Telegram channel: [@fansdeposit](https://t.me/fansdeposit)

## Environment Variables (already customized for you)

These must be set when deploying on Koyeb:

| Key               | Value                                                                 |
|------------------|-----------------------------------------------------------------------|
| `BOT_TOKEN`       | `8067339211:AAE-yvNtTRv7-O09YoIMi3qbYD23aw7v_vY`                     |
| `CHANNEL_USERNAME`| `@fansdeposit`                                                      |
| `GPLINKS_API`     | `eb820552d0f95f920542577393c3d88d6dbf6386`                          |
| `PASTELINK_API_KEY`| `bwecc2dqac9k9jk3vejjeqpfjnkwybpx7pwshccoqf5huuct9ud3w3awfqdbh7ryb763yjuqkbb` |

## Deployment on Koyeb

1. Fork or upload this repo to your GitHub.
2. Go to [https://app.koyeb.com](https://app.koyeb.com), create a new app.
3. Select your GitHub repo and connect it.
4. In "Build & Deploy":
   - **Build command:** leave blank
   - **Run command:** `./start.sh`
5. Add the above environment variables in the **Environment** tab.
6. Click **Deploy**. Your bot will go live!

## Files in Repo

- `main.py`: The Telegram bot logic
- `start.sh`: Starts the bot (used by Koyeb)
- `requirements.txt`: Python dependencies

## Notes

- The bot automatically runs 24/7.
- On first run, it fetches and processes the last 100 messages.
