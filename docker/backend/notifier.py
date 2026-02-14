import os
import logging
import httpx

logger = logging.getLogger(__name__)

async def send_telegram_review(metadata, file_name):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or "your_bot_token" in token:
        logger.warning("Telegram token not configured. Skipping review notification.")
        return True # Auto-approve if no token

    # Simplified: Sending a message with the extracted data
    # (In a real app, we'd use inline keyboards for Approve/Cancel)
    message = f"🔍 **Review New Device**\n\n"
    message += f"📄 File: {file_name}\n"
    message += f"🏷 Model: {metadata.get('model')}\n"
    message += f"🏭 Brand: {metadata.get('brand')}\n"
    message += f"🌍 Origin: {metadata.get('origin')}\n"
    message += f"💰 Price: {metadata.get('price_range')}\n\n"
    message += "Reply with 'OK' to save to Wiki."

    # Note: We need a Chat ID. For demo, we assume a bot command /start was sent to get it.
    # In Phase 1, we just log it or use a default if provided.
    logger.info(f"Telegram Review Sent: {metadata}")
    return True # Placeholder for auto-approve until bot command logic is added
