#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
replace coords with the cordinates of your location
replace token with your token
Usage:
Basic Echobot example, repeats messages.
/visible sends visible passes
/allpasses sends all passes
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from iss import get_passes
from datetime import date
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.



def send(bot, pass_data):
    
    
    
    message_string = ""
    if len(pass_data) > 0:
        dt = date.today().strftime("%Y-%m-%d")
        message_string = "{0} passes for today {1} \n \n".format((len(pass_data) + 1),dt)
        for i in pass_data:
            message_string += i[0] + "\n"
            message_string += i[1]
            message_string += "\n \n"
            
        bot.sendMessage(chat_id="@iss_noti",text=message_string)

        for image in pass_data:
            bot.sendPhoto(chat_id="@iss_noti",photo=open(image[2],"rb"))
















def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('''Hi! i'll text you the times iss passes over you \n
        /visible to get visible passes for and 
        /allpasses to get all passes today''')



def visible(bot, update):
    """send the visible passes for today"""
    update.message.reply_text('Calculating and sending todays visble passes')

    cords =[['6.5490 N','72.9534 E','vaikaradhoo'],['6.1497 N','73.2905 E','Funadhoo']]

    all_passes = []

    passes_morning = (get_passes(240,420,cords[1],date.today()))
    passes_evening = (get_passes(1050,1170,cords[1],date.today()))

    all_passes = passes_morning + passes_evening

    if len(all_passes) > 0:
        send(bot, all_passes)

    else:
        update.message.reply_text("No visible passes found for today")










def allpasses(bot,update):
    """send the visible passes for today"""
    update.message.reply_text('Calculating and sending todays all passes')

    cords =[['6.5490 N','72.9534 E','vaikaradhoo'],['6.1497 N','73.2905 E','Funadhoo']]

    

    all_passes = (get_passes(1,1440,cords[1],date.today()))

    if len(all_passes) > 0:
        send(bot, all_passes)

    else:
        update.message.reply_text("No  passes found for today")





def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher


    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("visible", visible))
    dp.add_handler(CommandHandler("allpasses",allpasses))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
    start()