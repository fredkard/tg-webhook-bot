"""
Telegram Webhook Bot Template
-----------------------------

This script provides a minimal webhook‑based Telegram bot built with aiogram
and aiohttp.  It registers a webhook on startup, defines a basic message
handler that echoes the incoming text, and listens for incoming HTTP POST
requests from Telegram.  It is suitable for deployment to services like
Render.com or Railway where only webhook‑based bots are allowed.

Environment variables:

* `BOT_TOKEN` – Telegram bot token (required)
* `BASE_WEBHOOK_URL` – base URL where the bot is hosted (e.g. https://your-domain.com)
* `WEBHOOK_PATH` – path for webhook endpoint (default: /webhook)
* `WEBHOOK_SECRET` – secret token used to verify incoming requests (optional)
* `PORT` – port to bind the aiohttp server (default: 8080)

For more details see README.md.
"""

import asyncio
import logging
import os
from typing import Optional

from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    """Register the webhook when the application starts."""
    webhook_url = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
    await bot.set_webhook(webhook_url, secret_token=WEBHOOK_SECRET or None)
    logger.info("Webhook set to %s", webhook_url)


async def on_shutdown(bot: Bot) -> None:
    """Delete the webhook when shutting down."""
    await bot.delete_webhook()
    logger.info("Webhook deleted")


async def handle_message(message: types.Message) -> None:
    """Personalized reply with user details."""
    first_name = message.from_user.first_name or "there"
    chat_id = message.chat.id
    username = message.from_user.username or "N/A"

    reply_text = (
        f"Hello {first_name},\n"
        f"Chat ID: {chat_id}\n"
        f"Username: {username}"
    )

    # Check if message is from a group or supergroup
    if message.chat.type in ["group", "supergroup"]:
        reply_lines.append(f"Group Chat ID: {message.chat.id}")

    # Check if message is forwarded from a channel
    if message.forward_from_chat and message.forward_from_chat.type == "channel":
        reply_lines.append(f"Forwarded from Channel ID: {message.forward_from_chat.id}")

    reply_text = "\n".join(reply_lines)
    await message.reply(reply_text)

async def main() -> None:
    # Load configuration from environment
    global BASE_WEBHOOK_URL, WEBHOOK_PATH, WEBHOOK_SECRET
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is required")
    BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL", "")
    if not BASE_WEBHOOK_URL:
        raise RuntimeError("BASE_WEBHOOK_URL environment variable must be set to your public HTTPS URL")
    WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")
    PORT = int(os.getenv("PORT", "8080"))

    # Initialize bot and dispatcher
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.message.register(handle_message)

    # Register startup and shutdown hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Create aiohttp application
    app = web.Application()
    # Set up webhook request handler
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET or None,
    )
    webhook_handler.register(app, path=WEBHOOK_PATH)
    # Mount dispatcher startup/shutdown hooks to the aiohttp app
    setup_application(app, dp, bot=bot)

    # Start the web server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=PORT)
    await site.start()

    logger.info("Bot is up and running. Listening on port %s", PORT)
    # Keep the server running
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
