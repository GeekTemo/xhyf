#!/usr/bin/env python
# encoding: utf-8

"""
@author: gongxingfa
@contact: siseulemen@gmail.com
@site: 
@software: PyCharm
@file: update_data.py
@time: 2018/11/30 11:11 PM
"""
import io
import re
import utils
import db_manager
from models import *


def line_info(line):
    line = line.strip()
    if not line:
        return {}
    ts = re.split('\s+', line)
    d = {}
    for t in ts:
        if utils.is_tel(t):
            d['tel'] = t
        elif utils.is_qq(t):
            d['qq'] = t
        elif utils.is_date(t):
            d['date'] = t
        elif t == '管理员':
            d['admin'] = t
        elif utils.is_zh(t):
            d['name'] = t
        elif utils.is_number(t):
            d['number'] = t
    return d


def read_lines_model(f, info_f, model_class, k_cols):
    """
    读取文件中每行的Model
    :param f: 文件名
    :param info_f: 每行用于提取信息的函数
    :param model_class: Model的类
    :param k_cols: 关键字字段
    :return:
    """
    k2m = {}
    with io.open(f, encoding='utf-8') as f:
        for line in f:
            m = model_class()
            d = info_f(line)
            if not d:
                continue
            utils.set_model_attrs(m, **d)
            k = tuple([getattr(m, c) for c in k_cols])
            if len(k) == 1:
                k = k[0]
            if k:
                if k in k2m:
                    m2 = k2m[k]
                    m = utils.merge_model(m2, m)
                k2m[k] = m
    return k2m


def update_contacts():
    tel2contacts = read_lines_model('data/contacts', line_info, Contacts, ['tel'])
    for tel, c in tel2contacts.items():
        c2 = db_manager.get_contacts_by_tel(tel)
        if c2:
            c = utils.merge_model(c2, c)
            c.save()
            utils.log_update_model(c)
        else:
            db_manager.create_model(c)
            utils.log_create_model(c)


def contacts_group():
    """联系人分组"""
    cts = [c for c in db_manager.get_all_contacts() if c.admin != '管理员']
    group_counts = {str(a.number): 0 for a in db_manager.get_all_admins()}
    for c in cts:
        a1 = None
        a2 = None
        if c.qq:
            a1 = db_manager.get_admin_by_qq(c.qq)
        if c.tel:
            a2 = db_manager.get_admin_by_tel(c.tel)
        a = a1 or a2
        if a:
            continue
        if c.group_number:
            group_counts[str(c.group_number)] += 1
        else:
            group_number = list(sorted(group_counts.items(), key=lambda pair: pair[1]))[0][0]
            c.group_number = str(group_number)
            group_counts[c.group_number] += 1
            c.save()
            utils.log_update_model(c)


def update_admins():
    qq2admins = read_lines_model('data/admins', line_info, Admins, ['qq'])
    for qq, a in qq2admins.items():
        a2 = db_manager.get_admin_by_qq(qq)
        if a2:
            a = utils.merge_model(a2, a)
            a.save()
            utils.log_update_model(a)
        else:
            db_manager.create_model(a)
            utils.log_create_model(a)


def update_actions():
    def action_line_info(line):
        d = line_info(line)
        if 'number' in d:
            d['numbers'] = d['number']
            del d['number']
        return d

    td2actions = read_lines_model('data/actions', action_line_info, Actions, ['tel', 'date'])
    for (tel, date), a in td2actions.items():
        if not a.numbers:
            a.numbers = 1
        a2 = db_manager.get_action_by_tel(tel, date)
        if a2:
            a = utils.merge_model(a2, a)
            a.save()
            utils.log_update_model(a)
        else:
            db_manager.create_model(a)
            utils.log_create_model(a)


def update_money():
    def money_line_info(line):
        d = line_info(line)
        if 'number' in d:
            d['money'] = d['number']
            del d['number']
        return d

    tel2moneys = read_lines_model('data/money', money_line_info, Money, ['tel'])
    for tel, m in tel2moneys.items():
        m2 = db_manager.get_money_by_tel(tel)
        if m2:
            m = utils.merge_model(m2, m)
            m.save()
            utils.log_update_model(m)
        else:
            db_manager.create_model(m)
            utils.log_create_model(m)


if __name__ == '__main__':
    update_contacts()
    update_admins()
    update_actions()
    update_money()
    contacts_group()
