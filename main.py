import discord
import os
from keep_alive import keep_alive
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode

intents = discord.Intents.default()
intents.members = True
client=discord.Client(intents=intents)    
TOKEN = os.environ.get('TOKEN')
CHANNEL = int(os.environ.get('CHANNEL'))
print(CHANNEL)

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def downloader(update, context):
	"""Download file from telegram"""
	x = context.bot.get_file(update.message.document).download()
	channel = client.get_channel(CHANNEL)
	client.loop.create_task(channel.send(file=discord.File(x)))

def echo(update, context):
    """Send message on telegram."""
    # update.message.reply_text(update.message.text)
    channel = client.get_channel(CHANNEL)
    print(channel)
    client.loop.create_task(channel.send(f"<{update.message.from_user.username}:>\n{update.message.text}"))
  

chat_id=os.environ.get('CHAT_ID')

updater = Updater(os.environ.get('TELEGRAM'),use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text, echo))
dispatcher.add_handler(MessageHandler(Filters.document, downloader))
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))


updater.start_polling()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_message(message):
    print(client.user)
    if message.attachments:
      for url in message.attachments: 
        updater.dispatcher.bot.send_message(chat_id=chat_id,text=f"{url}",parse_mode=ParseMode.HTML)

    if message.author != client.user:
      updater.dispatcher.bot.send_message(text=f"<{message.author}>: \n{message.content}",chat_id=chat_id)


keep_alive()
client.run(TOKEN)