import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG")

def clean_amazon_link(url):
    if "amazon" not in url:
        return None

    # togli parametri vecchi
    url = url.split("?")[0]

    if "/dp/" in url:
        asin = url.split("/dp/")[1].split("/")[0]
        return f"https://www.amazon.it/dp/{asin}/?tag={AFFILIATE_TAG}"

    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    new_link = clean_amazon_link(text)

    if not new_link:
        return

    await context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=f"🔥 OFFERTA AMAZON 🔥\n\n🛒 Acquista qui:\n{new_link}"
    )

    await update.message.reply_text("✅ Pubblicato nel canale!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot avviato...")
    app.run_polling()

if __name__ == "__main__":
    main()
