# -*- coding: utf8 -*-
from workdays_calendar.collection_names import CALENDAR_COLLECTION,TAGS_COLLECTION
from workdays_calendar.days_calendar import get_day_int
from workdays_calendar.tags import HOLIDAY_TAG
import datetime

def get_tag(db,tag_name):
    return db[TAGS_COLLECTION].find_one({'name': tag_name})

def day_has_tag(db,day,tag):
    if not tag:
        return False

    day_int=get_day_int(day)
    stored_day=db[CALENDAR_COLLECTION].find_one({'day_int': day_int})
    if stored_day:
        return str(tag['_id']) in stored_day['tags']
    return False

def is_holiday_today(db):
    holiday_tag=get_tag(db,HOLIDAY_TAG)
    return day_has_tag(db,datetime.date.today(),holiday_tag)

def get_workdays_interval(db,start,num_days):
    holiday_tag=get_tag(db,HOLIDAY_TAG)

    holidays_used=False
    total_days=0

    while day_has_tag(db,start,holiday_tag):
        start+=datetime.timedelta(days=1)
        holidays_used=True
        total_days+=1

    day=start
    drive_days=num_days
    while drive_days>0:
        day+=datetime.timedelta(days=1)
        total_days+=1
        if day_has_tag(db,day,holiday_tag):
            holidays_used=True
        else:
            drive_days-=1

    return {
        'end': day,
        'total_days': total_days,
        'holidays_used': holidays_used
    }
