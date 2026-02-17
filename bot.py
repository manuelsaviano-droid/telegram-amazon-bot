import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

def format_message(text):
    try:
        parts = text.split("\n")
        info = parts[0]
        link = parts[1].strip()

        prezzo_scontato, prezzo_vecchio, titolo = info.split("|")

        prezzo_scontato = float(prezzo_scontato.replace(",", "."))
        prezzo_vecchio = float(prezzo_vecchio.replace(",", "."))

        percentuale = round(((prezzo_vecchio - prezzo_scontato) / prezzo_vecchio) * 100)

        message = f"""🛍 Amazon 🇮🇹

💰 Scontata a {prezzo_scontato:.2f}€ ✅
❌ Invece di {prezzo_vecchio:.2f}€ (-{percentuale}%)

👉 {link}

📦 {titolo}

#affiliate"""

        return message

    except:
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    formatted = format_message(text)

    if not formatted:
        await update.message.reply_text("❌ Formato non corretto.\nUsa:\n79.99|139.99|Titolo\nlink")
        return

    await context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=formatted,
        disable_web_page_preview=False
    )

    await update.message.reply_text("✅ Pubblicato nel canale!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
