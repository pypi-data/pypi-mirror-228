# -*- coding: utf-8 -*-

from . import wh_setting,api_list

#WH2API - user.md

# 1. 이용자 목록 조회
def list():
    api = api_list.user_list
    result = wh_setting.get_requests(api=api)
    return result

# 1. 이용자 목록 조회 후 user_idx 조건 처리
def detail(user_idx):
    if type(user_idx) == int:
        user_idx = str(user_idx)

    user_list = list()
    user_list = user_list['users']
    user_detail = []
    for user in user_list:
        if user["idx"] == user_idx:
            user_detail = user
            return user_detail
        else:
            print("Not found.")
            return 'Not found.'

# 15. 보인 프로필 조회
def profile_read():
    api = api_list.user_profile_read
    result = wh_setting.get_requests(api=api)
    return result
