# -*- coding: utf8 -*-
import sys
import os
from pyramid.paster import bootstrap
from pymongo import MongoClient
import workdays_calendar.users
import workdays_calendar.tags
import workdays_calendar.days_calendar

db=None

def setup(settings):
    global db
    db=MongoClient(settings['mongo.uri'])[settings['mongo.db']]

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def run(settings):

    workdays_calendar.users.init_db(db,settings)
    
    workdays_calendar.tags.init_db(db,settings)

    workdays_calendar.days_calendar.init_db(db,settings)
    
def main():
    if 2!=len(sys.argv):
        usage(sys.argv)
    env = bootstrap(sys.argv[1])
    settings=env['registry'].settings
    setup(settings)

    run(settings)

if __name__=='__main__':
    main()
