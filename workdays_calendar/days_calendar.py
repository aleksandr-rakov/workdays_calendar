# -*- coding: utf8 -*-
import workdays_calendar.api as api
import calendar
import colander
import datetime
from workdays_calendar.collection_names import CALENDAR_COLLECTION,TAGS_COLLECTION


def init_db(db,settings):
    gen_year(db,datetime.datetime.now().year)

def chunkify(lst,n):
    return [ lst[i*n:i*n+n] for i in xrange(len(lst)/n) ]

def get_day_int(date):
    return date.year*10000+date.month*100+date.day

def gen_year(db,year):
    c=calendar.Calendar(0)

    holiday_tag=db[TAGS_COLLECTION].find_one({'name':'holiday'})

    if holiday_tag is None:
        print "Tag not found"
        return

    for m in xrange(1,13):
        for d,wd in c.itermonthdays2(year,m):
            if d and wd>=5:
                day_int=year*10000+m*100+d

                old=db[CALENDAR_COLLECTION].find_one({'day_int': day_int})
                if not old:
                    db[CALENDAR_COLLECTION].insert({
                            'day_int': day_int,
                            'tags': [str(holiday_tag['_id'])],
                        })

class StringList(colander.SequenceSchema):
    items = colander.SchemaNode(
            colander.String()
        )

class dayUpdataSchema(colander.Schema):
        tags = StringList()

class CalendarViews(api.BaseViews):

    @api.view(path='calendar/{year}', method='GET')
    def view_calendar(self):

        c=calendar.Calendar(0)
        year=int(self.params['year'])
        result=[]

        days=self.db[CALENDAR_COLLECTION].find({'$and':[
                {'day_int': {'$gte':year*10000}},
                {'day_int': {'$lte':(year+1)*10000}}
            ]})
        days=dict((x['day_int'],x.get('tags',[])) for x in days)
        for m in xrange(1,13):
            month=[]
            for d in c.itermonthdays(year,m):
                day_int=year*10000+m*100+d
                month.append({
                        'day': d,
                        'day_int': day_int,
                        'tags': days.get(day_int,[])
                    })
            weeks=chunkify(month,7)
            result.append({
                    'month': m,
                    'weeks': weeks
                })
        return result

    @api.view(path='calendar/day/{day_int}', method='POST')
    def view_day_change(self):
        schema=dayUpdataSchema()
        data=self.validated_data(schema)
        day_int=int(self.params['day_int'])
        self.db[CALENDAR_COLLECTION].update(
                {'day_int': day_int},
                {'$set': {
                    'tags': data['tags'],
                    'manual': True
                }},
                upsert=True
            )
