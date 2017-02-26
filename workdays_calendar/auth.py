# -*- coding: utf8 -*-
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow
import hashlib
from bson import ObjectId

LOGGED_IN_PERMISSION='admin'

class Hasher:
    #работа с подсолеными хешами
    @classmethod
    def salt(cls):
        return unicode(ObjectId())
    @classmethod
    def generate(cls,pw,salt=None):
        if salt==None:
            salt=ObjectId()
        return unicode(salt).encode('utf-8')+hashlib.md5(unicode(salt).encode('utf-8')+unicode(pw).encode('utf-8')).hexdigest()
    @classmethod
    def check(cls,pw_with_salt,pw):
        salt=pw_with_salt[:-32]
        return pw_with_salt==cls.generate(pw,salt)

def add_role_principals(userid, request):
    return ['role:%s'%LOGGED_IN_PERMISSION]

class RootFactory(object):
    def __init__(self, request):
        pass
    __acl__ = [
        (Allow, 'role:%s'%LOGGED_IN_PERMISSION, LOGGED_IN_PERMISSION),
    ]

def userid(request):
    try:
        return request.authenticated_userid
    except:
        return None

def has_perm(request):
    def has_perm(perm,context=None):
        if context is None:
            return request.has_permission(perm, request.context)
        else:
            return request.has_permission(perm, context)
    return has_perm

def includeme(config):

    config.set_root_factory(RootFactory)
    
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.include('pyramid_jwt')
    config.set_jwt_authentication_policy(
        'secret',
        http_header='X-Token',
        callback=add_role_principals
    )
    config.set_default_permission(LOGGED_IN_PERMISSION)

    config.add_request_method(userid,'userid', True, True)
    config.add_request_method(has_perm,'has_perm', True, True)
    