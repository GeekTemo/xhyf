#!/usr/bin/env python
# encoding: utf-8

"""
@author: gongxingfa
@contact: siseulemen@gmail.com
@site: 
@software: PyCharm
@file: models.py
@time: 2018/11/30 11:11 PM
"""

from peewee import *

database = MySQLDatabase('xuhui', **{'charset': 'utf8', 'use_unicode': True, 'user': 'root', 'password': 'Gxf921758'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Actions(BaseModel):
    date = CharField(null=True)
    numbers = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    qq = CharField(null=True)
    tel = CharField()

    class Meta:
        table_name = 'actions'


class Activity(BaseModel):
    att_date = CharField(null=True)
    attend = CharField(null=True)
    money = FloatField(null=True)
    qq = CharField(constraints=[SQL("DEFAULT '未知'")], null=True)
    tel = CharField(constraints=[SQL("DEFAULT '未知'")], null=True)

    class Meta:
        table_name = 'activity'


class Admins(BaseModel):
    id = IntegerField()
    name = CharField(null=True)
    number = IntegerField()
    qq = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    tel = CharField(constraints=[SQL("DEFAULT ''")], null=True)

    class Meta:
        table_name = 'admins'
        indexes = (
            (('id', 'number'), True),
        )
        primary_key = CompositeKey('id', 'number')


class Contacts(BaseModel):
    admin = CharField(null=True)
    group_number = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    house_number = CharField(null=True)
    name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    qq = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    tel = CharField()

    class Meta:
        table_name = 'contacts'


class Money(BaseModel):
    date = CharField(null=True)
    money = CharField(null=True)
    qq = CharField(null=True)
    tel = CharField(null=True)

    class Meta:
        table_name = 'money'


if __name__ == '__main__':
    c = Contacts()
    c.tel = '123456'
    print(type(c) == Contacts)
    e1 = getattr(Contacts, 'tel') == 'A'
    e2 = Contacts.tel == 'A'
    # print(getattr(Contacts, 'tel') == Contacts.tel)
    print(e1)
    print(e2)
