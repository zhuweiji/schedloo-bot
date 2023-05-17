import io
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List
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

from telegram_calendar.entities.calendar_entities import CalendarEvent, CalendarTime
from telegram_calendar.responses.callbacks.callbacks import Callback_Enum
from telegram_calendar.responses.commands.start import handle_command
from telegram_calendar.services.create_event import (
    create_new_event,
    create_new_telegram_event,
)
from telegram_calendar.services.telegram_bot_data import get_all_user_ids

log = logging.getLogger(__name__)



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    if not update.effective_chat: return
    if not update.message.text: return
    
    text = update.message.text 
    
    lines = text.splitlines()
    
    try:
        event, file = create_new_telegram_event(text,chat_id=update.effective_chat.id)
    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Expected a message with two/three lines, got {len(lines)} lines instead"
        )
        return 
    
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=file,
        caption=str(event),
    )

