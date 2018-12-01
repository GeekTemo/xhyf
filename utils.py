#!/usr/bin/env python
# encoding: utf-8

"""
@author: gongxingfa
@contact: siseulemen@gmail.com
@site: 
@software: PyCharm
@file: utils.py
@time: 2018/11/30 11:03 PM
"""
import re
from operator import truth
from playhouse.shortcuts import model_to_dict


def merge_model(old_model, new_model):
    m1_d = model_to_dict(old_model)
    m2_d = model_to_dict(new_model)
    for k in m1_d:
        v1 = m1_d.get(k)
        v2 = m2_d.get(k)
        v = v2 or v1
        setattr(old_model, k, v)
    return old_model


def set_model_attrs(model, **kwargs):
    for k, v in kwargs.items():
        if hasattr(model, k):
            setattr(model, k, v)


def is_number(s):
    s = s.strip()
    return truth(re.match("^\d+$", s))


def is_tel(s):
    s = s.strip()
    return s.startswith('1') and is_number(s) and len(s) == 11


def is_qq(s):
    s = s.strip()
    return is_number(s) and 5 <= len(s) < 11


def is_date(s):
    s = s.strip()
    return truth(s) and (
            re.match('^\d{4}-\d{2}-\d{2}', s) or re.match('^\d{2}-\d{2}$', s) or re.match('\d{4}/\d{2}/\d{2}', s))


def is_zh(s):
    for c in s:
        if not ('\u4e00' <= c <= '\u9fa5'):
            return False
    return True


def log_create_model(m):
    t = type(m)
    print('Create {}: {}'.format(t, model_to_dict(m)))


def log_update_model(m):
    t = type(m)
    print('Update {}: {}'.format(t, model_to_dict(m)))


if __name__ == '__main__':
    from models import *

    c1 = Contacts()
    c1.tel = '12343'
    c2 = Contacts()
    c2.qq = '2343'
    c3 = merge_model(c1, c2)
    print(c3.tel, c3.qq)
    print(is_zh('我是中国人'))
