"""responds to a start command sent by the user 
i.e. /start

provides information about the functions the bot provides"""

import io
import logging
from datetime import datetime, timedelta
from uuid import uuid4

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultDocument,
    InputFile,
    InputMediaDocument,
    InputTextMessageContent,
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
    MessageHandler,
    Updater,
    filters,
)

from telegram_calendar.responses.callbacks.callbacks import Callback_Enum

log = logging.getLogger(__name__)

EXAMPLE_EVENT_CREATE_MSG = """Amy's birthday
11/1 1pm
11/1 5pm"""

async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    
    
    await update.message.reply_text(
        text="""
Hello!
        
You can schedule events by sending me messages.
        
        """
    )
    
    await update.message.reply_text(
        text="""
If I receive a message with 2 lines,
1. Event name
2. Starting date/time

I will create an event file for you! You can send this to your friends or add it to your calendar.

You can add more lines, but this is optional:
3. Ending date/time
        """
    )
    
    keyboard = [
        [
            InlineKeyboardButton("Try me!", callback_data=Callback_Enum.SAMPLE_CREATE_NEW_MESSAGE_CALLBACK.name),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text=f"""
Here is an example:

{EXAMPLE_EVENT_CREATE_MSG}
        """
    , reply_markup=reply_markup)
    
    await update.message.reply_text(
        text="""
There are more functions available! /more
        """
    )
    
    await update.message.reply_text(
        text="""
You can see this message again by sending /help in the chat!
        """
    )

    return