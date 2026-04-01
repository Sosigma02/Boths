import hashlib
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =========================
# CONFIG
# =========================
BOT_TOKEN = "8695304067:AAE-pslrrnuCRliAY9Om9Qzl40QeEEFFVtM"

MCH_ID = "500258248"
SECRET_KEY = "IVI6KF0VHHWNXWWBJXB2OHM2GDPMMAQQ"

API_URL = "https://api.nekpayment.com/query/balance"


# =========================
# GENERATE SIGNATURE
# =========================
def generate_sign():
    sign_string = f"mch_id={MCH_ID}&key={SECRET_KEY}"
    return hashlib.md5(sign_string.encode()).hexdigest()


# =========================
# BALANCE COMMAND
# =========================
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        sign = generate_sign()

        post_data = {
            "sign_type": "MD5",
            "sign": sign,
            "mch_id": MCH_ID
        }

        response = requests.post(
            API_URL,
            data=post_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )

        if response.status_code == 200:
            await update.message.reply_text(f"Response:\n{response.text}")
        else:
            await update.message.reply_text(f"HTTP Error: {response.status_code}")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


# =========================
# START BOT
# =========================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("balance", balance))

print("Bot is running...")
app.run_polling()
