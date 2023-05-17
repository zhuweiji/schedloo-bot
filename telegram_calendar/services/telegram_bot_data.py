import io
import logging
from datetime import datetime, timedelta
from uuid import uuid4

from telegram import Update
from telegram.ext import ContextTypes

log = logging.getLogger(__name__)

def save_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat:
        # log.info(update)
        # log.info(context)
        log.warning("Unable to save user's chat id")
        return
    
    context.bot_data.setdefault("user_ids", set()).add(update.effective_chat.id)
    
    log.debug(f'saved user id {update.effective_chat.id}')
    
def get_all_user_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return context.bot_data.setdefault("user_ids", set())
    