"""responds to a start command sent by the user 
i.e. /start

provides information about the functions the bot provides"""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from telegram_calendar.responses.commands.start import EXAMPLE_EVENT_CREATE_MSG

log = logging.getLogger(__name__)

async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    
    await update.message.reply_text(
        text=f"""
If you're in a private chat with your friend or in a groupchat, you can create an event in that chat!
        """
    )

    await update.message.reply_text(
        text=f"""
Here's an example:

@{context.bot.username} {EXAMPLE_EVENT_CREATE_MSG}
ok
        """
    )
    
    await update.message.reply_text(
        text=f"""
        Do take note that I won't create the event until I see the word 'ok' on the last line!
        """
    )
    return