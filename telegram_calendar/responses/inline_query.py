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

from telegram_calendar.entities.calendar_entities import CalendarEvent, CalendarTime
from telegram_calendar.responses.callbacks.callbacks import (
    REGISTER_FOR_EVENT_TEXT,
    Callback_Enum,
)
from telegram_calendar.responses.commands.start import handle_command
from telegram_calendar.services.create_event import (
    create_new_event,
    create_new_telegram_event,
)

log = logging.getLogger(__name__)

async def handle_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle a inline query. This is run when you type: @botusername <query>"""
    
    if not update.inline_query: return 
    query = update.inline_query.query
    
    if not query: return # empty query should not be handled
    
    if not 'ok' in query.splitlines()[-1].lower():
        return
    else:
        query = '\n'.join(query.splitlines()[:-1])
    
    try:
        event, file = create_new_telegram_event(query, chat_id=update.inline_query.from_user.id)
    except ValueError as e:
        log.warning(e)
        return 
    
    keyboard = [
        [
            InlineKeyboardButton(REGISTER_FOR_EVENT_TEXT, callback_data=f'{REGISTER_FOR_EVENT_TEXT}{update.inline_query.from_user.id}'),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # create a new ics file and send it via PM to the user
    # this file is sent to telegram's server, and we can use it as a reply to the inline query
    message = await context.bot.send_document(
        chat_id=update.inline_query.from_user.id,
        document=file,
        caption=str(event),
    )
    
    if not message.document:
        log.warning('cannot get document of file sent to user')
        return
    
    file_id = message.document.file_id
    
    
    result = [
        InlineQueryResultDocument(
            id=str(uuid4()),
            title="Create Event",
            mime_type='application/octet-stream',
            document_url=file_id,
            caption=str(event),
            description=str(event),
            # reply_markup=reply_markup
        ),]
    
    
    await update.inline_query.answer(result)