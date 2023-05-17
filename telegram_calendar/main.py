import io
import logging
from datetime import datetime, timedelta
from pathlib import Path
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
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
    MessageHandler,
    PicklePersistence,
    TypeHandler,
    Updater,
    filters,
)

from telegram_calendar.entities.calendar_entities import CalendarEvent, CalendarTime
from telegram_calendar.responses import middleware
from telegram_calendar.responses.callbacks.callback_query import handle_callback_query
from telegram_calendar.responses.commands import more, start
from telegram_calendar.responses.error_handler import error_handler
from telegram_calendar.responses.inline_query import handle_inline_query
from telegram_calendar.responses.normal_messages import create_qianz_template, new_event

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
# assert (requests.get(url).json()), 'Failed to reach the telegram server'


if __name__ == "__main__":
    log.info(Path(__file__).parent / 'bot_data')
    persistence = PicklePersistence(filepath=Path(__file__).parent / 'bot_data')

    application = ApplicationBuilder().token(TOKEN).persistence(persistence).build()
    
    application.add_error_handler(error_handler)
    application.add_handler(TypeHandler(Update, middleware.pre_middleware),-1)
    
    
    application.add_handlers(handlers=[
            CommandHandler('help', start.handle_command),
            CommandHandler('start', start.handle_command),
            CommandHandler('more', more.handle_command),
            CommandHandler('more', more.handle_command),
            
            CallbackQueryHandler(handle_callback_query),
            InlineQueryHandler(handle_inline_query),
            
            MessageHandler(filters=filters.TEXT & filters.Regex('i am qianbub'), callback=create_qianz_template.handle_message),
            
            MessageHandler(filters=filters.TEXT & (~filters.COMMAND), callback=new_event.handle_message),
        ]
    )
    
    application.run_polling()
    
