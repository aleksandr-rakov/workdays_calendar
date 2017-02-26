# -*- coding: utf8 -*-
import workdays_calendar.api as api
import colander
from bson import ObjectId

_collection='tags'

@colander.deferred
def name_validator(node,kw):
    db=kw['db']
    tagid=kw['tagid']
    def validator(form, value):
        colander.Length(max=50)(form, value)
        if db[_collection].find_one({'name':value,'_id':{'$ne':tagid}}):
            raise colander.Invalid(
                    form, 
                    u'Тег с таким именем уже есть'
                )
    return validator

class TagsSchema(colander.Schema):
    name = colander.SchemaNode(
            colander.String(),
            validator=name_validator,
        )
    color = colander.SchemaNode(
            colander.String(),
        )

class TagsViews(api.BaseViews):

    @api.view(path='tags', method='GET')
    def view_tags(self):
        result=list(self.db[_collection].find({},{'password':0}).sort('name'))
        
        return result

    @api.view(path='tags', method='PUT')
    def view_tag_create(self):
        schema=TagsSchema().bind(
                db=self.db,
                tagid=None
            )
        data=self.validated_data(schema)
        self.db[_collection].insert(
            data
        )
        return {
            'message': u'Тег создан'
        }

    @api.view(path='tags/{tag_id}', method='POST')
    def view_tag_update(self):
        tagid=ObjectId(self.params['tag_id'])
        schema=TagsSchema().bind(
                db=self.db,
                tagid=tagid
            )
        data=self.validated_data(schema)
        self.db[_collection].update(
            {'_id': tagid},
            {'$set': data}
        )
        return {
            'message': u'Тег изменен'
        }
