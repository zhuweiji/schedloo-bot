import io
import logging
from datetime import datetime, timedelta
from enum import Enum
from uuid import uuid4

from telegram import (
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

from telegram_calendar.responses.callbacks.callbacks import (
    REGISTER_FOR_EVENT_TEXT,
    Callback_Enum,
)
from telegram_calendar.responses.commands.start import EXAMPLE_EVENT_CREATE_MSG
from telegram_calendar.services.create_event import (
    create_new_event,
    create_new_telegram_event,
)

log = logging.getLogger(__name__)


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    log.info(update)
    if not query: raise ValueError()
    
        
    log.info(query)
    log.info(query.data)
    
    
    if query.data == Callback_Enum.SAMPLE_CREATE_NEW_MESSAGE_CALLBACK.name:
        event, file = create_new_telegram_event(EXAMPLE_EVENT_CREATE_MSG, chat_id=query.from_user.id)
        await query.answer()
        
        await context.bot.send_document(
            chat_id=query.from_user.id,
            document=file,
            caption=str(event),
        )
        return
    
    elif query.data and REGISTER_FOR_EVENT_TEXT in query.data:
        chat_id = query.data.replace(REGISTER_FOR_EVENT_TEXT, '')
        if not update:  raise ValueError()
        if not update.callback_query: raise ValueError()
        if not context: raise ValueError()
        if not query: raise ValueError()
        if not query.data: raise ValueError()
        
        log.info(chat_id)
        
        
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=f'{update.callback_query.from_user.username} is coming!'
        )
        await query.answer()
        return
        
    # await query.edit_message_text(text=f"Selected option: {query.data}")

