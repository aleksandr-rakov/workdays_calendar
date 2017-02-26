# -*- coding: utf8 -*-
import colander
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from pyramid.decorator import reify
from pyramid.i18n import get_localizer

def translate(request):
    def translator(msg):
        if msg=="":
            return ""
        elif hasattr(msg, 'interpolate'):
            return get_localizer(request).translate(msg)
        else:
            return msg
    return translator

API_VERSION='1'
API_PREFIX='api/v%s/'%API_VERSION

class view(view_config):

    def __call__(self, wrapped):
        settings = self.__dict__.copy()
        depth = settings.pop('_depth', 0)

        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            
            # ===========our part start============
            route_name="%s_%s"%(name,wrapped.__name__)
            view_keys={
                'permission':'permission',
            }
            view_settings=dict((key2,settings[key1]) for key1,key2 in view_keys.items() if key1 in settings)
            if config.registry.settings.get('check_xsrf')=='true':
                view_settings['check_xsrf']=settings.get('check_xsrf',True)

            route_keys={
                'method': 'request_method'
            }
            route_settings=dict((key2,settings[key1]) for key1,key2 in route_keys.items() if key1 in settings)
            route_settings['pattern']="%s%s"%(API_PREFIX,settings['path'])

            config.add_route(route_name, **route_settings)
            config.add_view(view=ob, attr=wrapped.__name__, route_name=route_name, renderer='json', **view_settings)
            # ===========our part end==============

        info = self.venusian.attach(wrapped, callback, category='pyramid',
                                    depth=depth + 1)

        if info.scope == 'class':
            if settings.get('attr') is None:
                settings['attr'] = wrapped.__name__

        settings['_info'] = info.codeinfo # fbo "action_method"
        return wrapped

class BaseViews(object):
    def __init__(self, context, request):
       self.context = context
       self.request = request
       self.db=request.db
       self.initialize()
    
    def initialize(self):
        pass

    @reify
    def modifers(self):
        return self.request.GET

    @reify
    def params(self):
        return self.request.matchdict

    @reify
    def data(self):
        return self.request.body and self.request.json_body or {}

    def validate(self,schema,data):
        try:
            return schema.deserialize(data)
        except colander.Invalid as e:
            raise ValidationFailure(e.asdict(translate(self.request)))
    
    def validated_data(self,schema):
        return self.validate(schema,self.data)
    
class ValidationFailure(Exception):
    def __init__(self, data):
        self.data = data

@view_config(context=ValidationFailure, renderer='json', permission=NO_PERMISSION_REQUIRED)
def failed_validation(exc, request):
    request.response.status_int = 422
    return {'errors': exc.data}
