import logging
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Union

import dateparser
import parsedatetime
import pytz
from icalendar import Calendar, Event
from pytz import timezone

log = logging.getLogger(__name__)

@dataclass
class CalendarTime:
    dateTime: datetime
    timezone_offset = '+0800'
    
    def __init__(self, datetime) -> None:
        log.debug(datetime)
        
        if isinstance(datetime, str): datetime = self.add_colon_to_time(datetime)
        log.debug(datetime)
        
        parsed_datetime =  self.parse_datetime_to_iso(datetime)
        log.debug(datetime)
        
        if not parsed_datetime: raise ValueError
        self.dateTime = parsed_datetime

    def __bool__(self): return bool(self.dateTime)
    
    def __str__(self) -> str:
        return self.dateTime.strftime("%a, %d/%m %I:%M %p")
    
    @classmethod
    def parse_datetime_to_iso(cls, datetime_str):
        if isinstance(datetime_str, datetime): 
            return datetime_str
        
        parsed_datetime = dateparser.parse(
            f'{datetime_str} {cls.timezone_offset}', settings={'DATE_ORDER': 'DMY', 'RELATIVE_BASE': datetime.now()}
        )
        
        if not parsed_datetime:
            date_regex = r'(.*)?(\d?\d)\/(/d?/d)(\/\d\d\d?\d?)?(.*)?'
            datetime_str = re.sub(date_regex, r'\1 \3\/\2\/\4 \5', datetime_str) # flip months and dates for the parsedatetime library, which expects mm/dd
            calendar = parsedatetime.Calendar()
            parsed_datetime = calendar.parseDT(datetimeString=datetime_str, tzinfo=timezone('Asia/Singapore'))[0]
        
        if not parsed_datetime:
            raise ValueError
        
        if any(i in datetime_str.lower() for i in ['tmr','tommorow']): # both libraries don't handle the tommorow word well
            if (parsed_datetime - timedelta(days=1)).day != datetime.now().day:
                parsed_datetime = parsed_datetime.replace(day=datetime.now().day + 1)
            
        
        return parsed_datetime
    
    @classmethod
    def add_colon_to_time(cls, datetime_str):
        
        #not-number? start-time end-time am/pm others
        date_string = r'(\d{1,2}?\/\d\d)'
        
        am_pm_string = r'(AM|PM|am|pm)'
        time_string = r'(\d{1,4})' + am_pm_string 
        
        final_regex = rf'([^\d.]*){date_string}\s{time_string}(.*)'
        log.debug(final_regex)
        log.info(datetime_str)
        
        if match := re.search(final_regex, datetime_str):
            user_time_portion = match.group(3)
            if len(user_time_portion) > 4:
                raise ValueError('Parsed time passed by user has more than 4 values')
            if len(user_time_portion) == 3:
                user_time_portion = f"{user_time_portion[0]}:{user_time_portion[1:]}"
            elif len(user_time_portion) == 4:
                user_time_portion = f"{user_time_portion[0:2]}:{user_time_portion[2:]}"
        
            return re.sub(final_regex, fr'\1 \2 {user_time_portion}\4 \5', datetime_str)
        else:
            return datetime_str
    
    def asdict(self):
        return {"dateTime": str(self.dateTime.isoformat()), "timeZone": 'Asia/Singapore'}
    

@dataclass
class CalendarEvent:
    name:  str
    start: Union[CalendarTime, str]
    end:   Union[CalendarTime, str]

    location:    str = ''
    description: str = ''

    calendarId: str = 'primary'
    sendUpdates: str = 'false'
    
    attribute_to_description_map = {
        "name": "The name/description of the event",
        "start": "The starting date and time of the event - eg. 10 May 10:00PM",
        "end": "The ending date and time of the event - eg. 15 May 8:00AM\n",
        "location [optional]":  "The location of the event",
        "description [optional]": "A description of the event",
        "sendUpdates [optional]": "this feature is WIP"
    }
    
    def __post_init__(self):
        # probably can skip the asdict calls on the start,end attributes since asdict calling asdict on this datacalss will act recursively on all attrs
        if isinstance(self.start, str): self.start = CalendarTime(self.start)
        if isinstance(self.end, str): self.end = CalendarTime(self.end)
        
    def to_ics(self):
        event = Event()
        cal = Calendar()
        
        event.add('summary', self.name)
        
        if isinstance(self.start, str) or isinstance(self.end, str):
            raise ValueError
        
        event.add('dtstart', self.start.dateTime)
        event.add('dtend', self.end.dateTime)
        event.add('DTSTAMP', datetime.now())
        
        cal.add_component(event)
        
    
        return cal.to_ical()
    
    def __str__(self) -> str:
        return f"Event: {self.name}\nFrom: {self.start}\nTill: {self.end}"
        
    
class EventCreationError(Exception): 
    def __init__(self, message='', errors:dict={}):            
        super().__init__(message)
        self.errors = errors
    
    def __str__(self) -> str:
        return str(self.errors)