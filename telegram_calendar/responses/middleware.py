import logging

from telegram import Update
from telegram.ext import ContextTypes

from telegram_calendar.services.telegram_bot_data import save_user_id

log = logging.getLogger(__name__)

async def pre_middleware(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user_id(update, context)
    
    return