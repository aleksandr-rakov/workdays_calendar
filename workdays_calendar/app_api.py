# -*- coding: utf8 -*-
from workdays_calendar.collection_names import CALENDAR_COLLECTION,TAGS_COLLECTION
from workdays_calendar.days_calendar import get_day_int
from workdays_calendar.tags import HOLIDAY_TAG
import datetime


def is_holiday(db,day):
    holiday_tag=db[TAGS_COLLECTION].find_one({'name': HOLIDAY_TAG})
    if not holiday_tag:
        return False

    day_int=get_day_int(day)
    stored_day=db[CALENDAR_COLLECTION].find_one({'day_int': day_int})
    if stored_day:
        return str(holiday_tag['_id']) in stored_day['tags']
    return False

def get_workdays_interval(db,start,num_days):
    reached=0
    day=start
    while reached!=num_days:
        if not is_holiday(db,day):
            reached+=1
        day+=datetime.timedelta(days=1)
    return day
