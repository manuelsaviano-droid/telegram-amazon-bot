import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")


def format_price(price):
    return f"{price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def build_message(text):
    try:
        lines = text.strip().split("\n")

        if len(lines) < 2:
            return None

        info = lines[0]
        link = lines[1].strip()

        prezzo_scontato, prezzo_vecchio, titolo = info.split("|")

        prezzo_scontato = float(prezzo_scontato.replace(",", "."))
        prezzo_vecchio = float(prezzo_vecchio.replace(",", "."))

        percentuale = round(((prezzo_vecchio - prezzo_scontato) / prezzo_vecchio) * 100)

        prezzo_scontato_str = format_price(prezzo_scontato)
        prezzo_vecchio_str = format_price(prezzo_vecchio)

        message = f"""🛍 <b>Amazon</b> 🇮🇹

💰 <b>Scontata a {prezzo_scontato_str}€</b> ✅
❌ Invece di {prezzo_vecchio_str}€ (-{percentuale}%)

📦 <b>{titolo}</b>

#affiliate
"""

        final_message = message + "\n" + link

        return final_message

    except:
        return None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    formatted = build_message(update.message.text)

    if not formatted:
        await update.message.reply_text(
            "❌ Formato non corretto.\n\nUsa:\n79.99|139.99|Titolo prodotto\nhttps://amazon.it/link"
        )
        return

    await context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=formatted,
        parse_mode="HTML",
        disable_web_page_preview=False
    )

    await update.message.reply_text("✅ Pubblicato nel canale!")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot avviato...")
    app.run_polling()


if __name__ == "__main__":
    main()
