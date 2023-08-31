# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : main.py
@Date    : 2023/8/28 11:38:52
@Author  : zhchen
@Desc    : 
"""
from test.__test import open_elihu


def test_no_long_account_id():
    r1 = open_elihu.call_get_shovel_request_related_accounts("*", "TMALL-BACK")
    print(r1)
    print(r1.text)


if __name__ == '__main__':
    test_no_long_account_id()
