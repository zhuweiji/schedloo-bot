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

log = logging.getLogger(__name__)

import calendar
import datetime


def generate_schedlo_template():
    # Get the current date
    today = datetime.date.today()

    # Get the first day of the next month
    next_month = today.replace(day=1) + datetime.timedelta(days=32)
    next_month = next_month.replace(day=1)

    # Get the calendar for the next month
    cal = calendar.monthcalendar(next_month.year, next_month.month)

    # Define the list of weekdays
    weekdays = ['mon', 'tues', 'weds', 'thurs', 'fri', 'sat', 'sun']

    # Generate the string for each day in the next month
    text = f"{calendar.month_name[next_month.month]}/{next_month.year}\n" + '-'*20 + '\n'
    for week in cal:
        for i, day in enumerate(week):
            if day != 0:
                day_of_week = weekdays[i]
                day_str = f"{day} {day_of_week:}"
                text += f"{day_str:<6} -\n"
                if day_of_week == 'sun': text += '\n'
    return text

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    
    await update.message.reply_text(
        text=f"""
        Hi qianbub!! Here is a schedlo template:
        """
    )
    
    await update.message.reply_text(
        text=generate_schedlo_template()
    )

    return

