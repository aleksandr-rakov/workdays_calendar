# -*- coding: utf8 -*-
import workdays_calendar.api as api
import colander
from pyramid.httpexceptions import HTTPNotFound
from bson import ObjectId
from time import sleep
from workdays_calendar.auth import Hasher
from pyramid.security import NO_PERMISSION_REQUIRED

_collection='users'

def authenticate(request,login,password):
    userid=None
    message=''
    if request.userid:
        message='Already logged in'
    if login and password:
        user=request.db[_collection].find_one({'login':login})
        if user and Hasher.check(user['password'],password):
            if user['disabled']:
                message = u'Аккаунт заблокирован'
            else:
                userid=str(user['_id'])
                message=''
        else:
            message = u'Ошибка! Проверьте правильнось ввода логина и пароля'
            sleep(1) #затрудним перебор пароля
    else:
        message=u'Введите логин и пароль'

    return userid,message

class updatePasswordSchema(colander.Schema):
    password = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5)
    )

@colander.deferred
def login_validator(node,kw):
    db=kw['db']
    userid=kw['userid']
    def validator(form, value):
        colander.Length(max=50)(form, value)
        """Проверяем не занят ли логин"""
        if db[_collection].find_one({'login':value,'_id':{'$ne':userid}}):
            raise colander.Invalid(
                    form, 
                    u'Этот логин уже зарегистрирован'
                )
    return validator

class updateUserSchema(colander.Schema):
    name = colander.SchemaNode(
            colander.String(),
        )
    login = colander.SchemaNode(
            colander.String(),
            validator=login_validator,
        )
    disabled = colander.SchemaNode(
            colander.Bool(),
        )

class createUserSchema(updateUserSchema,updatePasswordSchema):
    pass

class UsersViews(api.BaseViews):

    @api.view(path='login', method='POST',permission=NO_PERMISSION_REQUIRED)
    def login(self):
        login = self.data['login']
        password = self.data['password']
        message=''

        user_id,message = authenticate(self.request, login, password)
        if user_id:
            return {
                'token': self.request.create_jwt_token(user_id)
            }
        if message:
            self.request.response.status=401
        return {
            'message': message
        }

    @api.view(path='profile', method='GET')
    def profile(self):
        userid=self.request.userid
        user=self.db[_collection].find_one({'_id':ObjectId(userid)})
        return {
            'userid': userid,
            'name': user['name']
        }

    @api.view(path='users', method='GET')
    def view_users(self):

        result=list(self.db[_collection].find({},{'password':0}).sort('name'))
        
        return result

    @api.view(path='users/{user_id}', method='GET')
    def view_user(self):
        user=self.db[_collection].find_one({'_id': ObjectId(self.params['user_id'])})
        user['password']=''
        if user is None:
            raise HTTPNotFound()
        return user

    @api.view(path='users', method='PUT')
    def view_user_create(self):
        schema=createUserSchema().bind(
                db=self.db,
                userid=None
            )
        data=self.validated_data(schema)
        data['password']=Hasher.generate(data['password'])
        self.db[_collection].insert(
            data
        )
        return {
            'message': u'Пользователь создан'
        }

    @api.view(path='users/{user_id}', method='POST')
    def view_user_update(self):
        userid=ObjectId(self.params['user_id'])
        schema=updateUserSchema().bind(
                db=self.db,
                userid=userid
            )
        data=self.validated_data(schema)
        self.db[_collection].update(
            {'_id': userid},
            {'$set': data}
        )
        return {
            'message': u'Пользователь изменен'
        }

    @api.view(path='users/{user_id}/change_password', method='POST')
    def view_user_change_pasword(self):
        userid=ObjectId(self.params['user_id'])
        schema=updatePasswordSchema()
        data=self.validated_data(schema)
        data['password']=Hasher.generate(data['password'])
        self.db[_collection].update(
            {'_id': userid},
            {'$set': data}
        )
        return {
            'message': u'Пароль изменен'
        }
