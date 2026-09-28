import os
import telebot
import google.generativeai as genai
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Render के लिए डमी वेब सर्वर ताकि पोर्ट एरर न आए
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive and running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# वेब सर्वर को बैकग्राउंड में शुरू करना
threading.Thread(target=run_web_server, daemon=True).start()

# API Keys प्राप्त करना
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "नमस्ते! मैं आपका एआई बॉट हूँ। मुझसे कोई भी सवाल पूछिए!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message,         bot.reply_to(message, f"Error: {e}")


print("Bot is starting...")
bot.infinity_polling()
