#!/usr/bin/env python
# encoding: utf-8

"""
@author: gongxingfa
@contact: siseulemen@gmail.com
@site: 
@software: PyCharm
@file: db_manager.py
@time: 2018/11/30 11:13 PM
"""
from models import *
from playhouse.shortcuts import model_to_dict


def get_all_contacts():
    """
    所有联系人名单
    :return:
    """
    return list(Contacts.select())


def get_contacts_by_tel(tel):
    cs = list(Contacts.select().where(Contacts.tel == tel))
    if cs:
        return cs[0]
    else:
        return None


def get_all_admins():
    return Admins.select()


def get_admin_by_tel(tel):
    admins = list(Admins.select().where(Admins.tel == tel))
    if admins:
        return admins[0]
    else:
        return None


def get_admin_by_qq(qq):
    admins = list(Admins.select().where(Admins.qq == qq))
    if admins:
        return admins[0]
    else:
        return None


def get_money_by_tel(tel):
    moneys = list(Money.select().where(Money.tel == tel))
    if moneys:
        return moneys[0]
    else:
        return None


def get_action_by_tel(tel, date):
    actions = list(Actions.select().where(Actions.tel == tel, Actions.date == date))
    if actions:
        return actions[0]
    else:
        return None


def create_model(m):
    d = model_to_dict(m)
    t = type(m)
    t.create(**d)


if __name__ == '__main__':
    a = Actions()
    a.tel = '12345678901'
    a.qq = '1111111111'
    a.date = '2018-11-26'
    # create_model(a)
    print(model_to_dict(a))
