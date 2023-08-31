# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : __test.py.py
@Date    : 2023/8/25 13:08:03
@Author  : zhchen
@Desc    : 
"""
import json

from hertz_packet.notice import get_kv

from open_elihu import OpenElihuBox

COOKIES = json.loads(get_kv("leqee_zhchen_cookie")['memo'])

print(COOKIES)
BIDP_COOKIES = COOKIES
ELIHU_COOKIES = COOKIES
OC_COOKIES = COOKIES

open_elihu = OpenElihuBox(tp_code='zhchen8', tp_secret="TinSyouSunSky")
