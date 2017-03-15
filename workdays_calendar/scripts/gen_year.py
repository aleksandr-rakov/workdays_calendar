# -*- coding: utf8 -*-
import sys
import os
from pyramid.paster import bootstrap
from pymongo import MongoClient
from workdays_calendar.days_calendar import gen_year

db=None

def setup(settings):
    global db
    db=MongoClient(settings['mongo.uri'])[settings['mongo.db']]

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <year> <config_uri>\n'
          '(example: "%s 2017 development.ini")' % (cmd, cmd))
    sys.exit(1)

def run(settings,year):
    gen_year(db,year)
    
def main():
    if 3!=len(sys.argv):
        usage(sys.argv)
    env = bootstrap(sys.argv[2])
    settings=env['registry'].settings
    setup(settings)

    year=int(sys.argv[1])
    run(settings,year)

if __name__=='__main__':
    main()
