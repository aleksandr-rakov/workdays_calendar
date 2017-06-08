# -*- coding: utf8 -*-
from workdays_calendar.collection_names import CALENDAR_COLLECTION,TAGS_COLLECTION
from workdays_calendar.days_calendar import get_day_int
from workdays_calendar.tags import HOLIDAY_TAG
import datetime

def get_holiday_tag(db):
    return db[TAGS_COLLECTION].find_one({'name': HOLIDAY_TAG})

def is_holiday(db,day,holiday_tag=None):
    if holiday_tag is None:
        holiday_tag=get_holiday_tag(db)
    if not holiday_tag:
        return False

    day_int=get_day_int(day)
    stored_day=db[CALENDAR_COLLECTION].find_one({'day_int': day_int})
    if stored_day:
        return str(holiday_tag['_id']) in stored_day['tags']
    return False

def is_holiday_today(db):
    return is_holiday(db,datetime.date.today())

def get_workdays_interval(db,start,num_days):
    holiday_tag=get_holiday_tag(db)

    holidays_used=False
    total_days=0

    while is_holiday(db,start,holiday_tag):
        start+=datetime.timedelta(days=1)
        holidays_used=True
        total_days+=1

    day=start
    drive_days=num_days
    while drive_days>0:
        day+=datetime.timedelta(days=1)
        total_days+=1
        if is_holiday(db,day,holiday_tag):
            holidays_used=True
        else:
            drive_days-=1

    return {
        'end': day,
        'total_days': total_days,
        'holidays_used': holidays_used
    }
