import io
import logging
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Dict, List, Set

from telegram_calendar.entities.calendar_entities import CalendarEvent, CalendarTime
from telegram_calendar.services.telegram_bot_data import get_all_user_ids

log = logging.getLogger(__name__)


@dataclass
class TelegramEventObject:
    chat_id: int
    event: CalendarEvent
    attending: Set = field(default_factory=lambda: set())
    
    def __hash__(self) -> int:
        return hash(f'{self.chat_id} {self.event}')
    

class EventTracker:
    events_created:Set[TelegramEventObject] = set()
    
    @classmethod
    def add_event(cls, telegramEventObject: TelegramEventObject):
        cls.events_created.add(telegramEventObject)
        log.info(telegramEventObject)
    
def create_new_telegram_event(text:str, chat_id:int):
    event, file = create_new_event(text)
    t_event = TelegramEventObject(event=event, chat_id=chat_id)
    EventTracker.add_event(t_event)
    return event, file
    

def create_new_event(text: str):
    lines = text.splitlines()
    
    if len(lines) == 2: # create event with name and start datetime, and end as one hour after
        event_name, start_date = lines
        start_date = CalendarTime(start_date)
        end_date = CalendarTime(start_date.dateTime + timedelta(hours=1))
        
    elif len(lines) == 3:
        event_name, start_date, end_date = lines
        start_date = CalendarTime(start_date)
        end_date = CalendarTime(end_date)
        if end_date.dateTime.date() < start_date.dateTime.date():
            end_date.dateTime = end_date.dateTime.replace(day=start_date.dateTime.day, month=start_date.dateTime.month, year=start_date.dateTime.year)
        
    else:
        raise ValueError("Expected a message with two/three lines, got {len(lines)} lines instead")
    
    log.debug(lines)
    log.debug(start_date)
    log.debug(end_date)
    
        
    event = CalendarEvent(name=event_name, start=start_date, end=end_date)
    data = event.to_ics()
    file = io.BytesIO(data)
    file.name = f'{event_name}.ics'
    
    return event, file