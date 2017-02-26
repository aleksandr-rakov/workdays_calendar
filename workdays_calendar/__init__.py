# -*- coding: utf8 -*-
from pyramid.config import Configurator
from bson.objectid import ObjectId
import datetime
from pyramid.renderers import JSON
from pyramid.events import NewRequest
from pymongo import MongoClient

def add_request_properties(event):
    """Сделаем некоторые параметры конфигурации атрибутами request"""
    reg = event.request.registry
    event.request.db=reg.db

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    mongo_conn = MongoClient(settings['mongo.uri'])
    mongo_db=mongo_conn[settings['mongo.db']]
    config.registry.db=mongo_db
    config.add_subscriber(add_request_properties,NewRequest)

    def datetime_adapter(obj, request):
        return obj.isoformat()+'Z'
    def objectid_adapter(obj, request):
        return str(obj)

    renderer = JSON(ensure_ascii=False,indent=4)
    renderer.add_adapter(datetime.datetime, datetime_adapter)
    renderer.add_adapter(ObjectId, objectid_adapter)
    config.add_renderer('json', renderer)

    config.include('workdays_calendar.auth')
    config.scan()
    
    return config.make_wsgi_app()
