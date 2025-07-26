# Telegram Webhook Bot Template

This repository is a minimal template for building Telegram bots using
[`aiogram`](https://docs.aiogram.dev/) with a webhook instead of long polling.  It includes a basic echo handler, webhook setup via `aiohttp` and guidance for deploying on popular PaaS platforms such as Render.com or Railway.

## Purpose

Deploying a Telegram bot on a server requires using webhooks rather than polling, because polling can be inefficient and is blocked on some hosting providers.  According to the aiogram documentation, when you configure a webhook Telegram will push updates to your URL, and you cannot use long polling at the same time【471498544294698†L576-L599】.  This template demonstrates how to register a webhook and set up an asynchronous HTTP server to receive updates.

## Technology Stack

* **Python 3**
* **aiogram 3** – modern asynchronous Telegram bot framework
* **aiohttp** – lightweight asynchronous web server used for the webhook endpoint

## Local Setup

1. Clone the repository and install dependencies:

   ```bash
   git clone https://github.com/your‑username/tg-webhook-bot.git
   cd tg-webhook-bot
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create a bot with [@BotFather](https://t.me/BotFather) and obtain the token.

3. Define environment variables (in `.env` or via your hosting dashboard):

   - `BOT_TOKEN` – token issued by BotFather
   - `BASE_WEBHOOK_URL` – public domain with HTTPS (e.g. `https://your-subdomain.onrender.com`)
   - `WEBHOOK_PATH` – path on which to accept requests (default `/webhook`)
   - `WEBHOOK_SECRET` – secret token used to verify Telegram’s requests (optional but recommended)
   - `PORT` – port for the local server (Render uses `$PORT` automatically)

4. Run the bot locally using a tool like [`ngrok`](https://ngrok.com/) to expose your local server, set `BASE_WEBHOOK_URL` to the public ngrok URL and start the script:

   ```bash
   python main.py
   ```

## Deployment on Render or Railway

1. Push this repository to your GitHub account.
2. Create a new web service on Render.com or Railway with the following settings:
   * **Runtime**: Python 3
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `python main.py`
   * **Environment Variables**: set `BOT_TOKEN`, `BASE_WEBHOOK_URL` (your Render domain), `WEBHOOK_PATH` (e.g. `/webhook`), and `WEBHOOK_SECRET`.
3. For Render, you don’t need to specify a port; use the `$PORT` environment variable automatically provided by the platform.  The script will register the webhook on startup.

## Demonstration idea (≤2 min)

1. Record a video showing how you create a new service on Render, set environment variables and deploy the bot.
2. Use ngrok or Render’s public URL to send a `/start` message to your bot and observe the echo reply.
3. Highlight how quickly the bot is online once the webhook is registered.

## Opportunities for improvement

* **Custom handlers** – add command handlers, inline keyboards, middleware, etc.
* **Persistent storage** – integrate with a database (e.g. PostgreSQL) for storing user data.
* **API token rotation** – implement secret rotation for enhanced security.
* **Multiple bots** – use `TokenBasedRequestHandler` from aiogram to host multiple bots on a single service.

## Helpful note on webhooks

When using webhooks with aiogram you should run your bot inside an asynchronous web framework such as `aiohttp`.  The library provides ready‑made request handlers to register your webhook and automatically respond to Telegram.  The documentation highlights that you can’t use long polling and webhooks concurrently【471498544294698†L576-L599】, so this template sticks strictly to the webhook approach.
