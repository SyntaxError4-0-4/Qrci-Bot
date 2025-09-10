# Gerekli kütüphaneleri ekle
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import qrcode
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasını yükler

BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start komutu için özel mesaj
def start(update, context):
    update.message.reply_text("Merhaba! QR kod oluşturmak için bana bir şeyler yaz 😎")

# Normal mesajları QR'a çevir
def qr_uret(update, context):
    mesaj = update.message.text

    # QR kod oluştur
    qr = qrcode.make(mesaj)

    # QR kodu geçici belleğe kaydet
    hafiza = BytesIO()
    hafiza.name = 'qr.png'
    qr.save(hafiza, 'PNG')
    hafiza.seek(0)

    # QR kodu kullanıcıya gönder
    update.message.reply_photo(photo=hafiza, caption="İşte QR kodun!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # /start komutu için ayrı işlem
    dp.add_handler(CommandHandler("start", start))

    # Diğer yazılı mesajlar için QR üret
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, qr_uret))

    print("Bot çalışıyor...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()