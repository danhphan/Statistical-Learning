#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.

This program is dedicated to the public domain under the CC0 license.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from uuid import uuid4

from telegram.utils.helpers import escape_markdown

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler,  Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import json
import pymssql
import datetime


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi mate. Use /set <hours> <postcode> to set a timer and a location for listing views :)')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo every messages"""
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


repeat_hour = 1
post_code = ""
def set_timer(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""

    keyboard = [[InlineKeyboardButton("City views", callback_data='1'),
                 InlineKeyboardButton("Sea views", callback_data='2')],
                [InlineKeyboardButton("Lake views", callback_data='3'),
                InlineKeyboardButton("Any views", callback_data='4')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    try:
        # args[0] should contain the time for the timer in seconds
        global repeat_hour
        repeat_hour = int(args[0])
        global post_code
        post_code = args[1]
        if repeat_hour < 0:
            update.message.reply_text('Sorry we can not go back to the past!')
            return

        # Add job to queue
        #job = job_queue.run_once(send_listing, due, context=chat_id)
        #job = job_queue.run_repeating(send_listing_vews, due, context=chat_id)

       # update.message.reply_text('Timer successfully set!')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <hours>')


def button(bot, update, job_queue, chat_data):
    query = update.callback_query
    bot.edit_message_text(text="Successfully set",
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    # Update Views type
    global view_type
    global repeat_hour
    print("REPEAT HOURS: " + str(repeat_hour))
    view_type = int(format(query.data))
    chat_id = query.message.chat_id
    job = job_queue.run_repeating(send_listing_vews, repeat_hour * 60, first=1, context=chat_id)
    chat_data['job'] = job

def unset(bot, update, job_queue, chat_data):
    """Remove the job if the user changed their mind."""
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return
    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']
    del job

    update.message.reply_text('Timer successfully unset!')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text = "Sorry, I didn't understand it")

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler('caps', caps, pass_args=True))
    dp.add_handler(CommandHandler('get_listing', get_listing, pass_args=True))
    dp.add_handler(CommandHandler("set", set_timer, pass_args=True, pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_handler(CallbackQueryHandler(button, pass_job_queue=True, pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
