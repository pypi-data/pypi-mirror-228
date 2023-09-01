# -*- coding: utf-8 -*-

from . import wh_setting, api_list


#WH2API - mytask.md

#1. To-Do 조회
def todo(observed_user_idx=""):
    api = api_list.mytask_todo
    result = wh_setting.get_requests(api=api,observed_user_idx = observed_user_idx)
    return result

#2. In-Progress 조회
def inprogress(last="",observed_user_idx=""):
    api = api_list.mytask_inprogress %(last)
    result = wh_setting.get_requests(api=api,observed_user_idx = observed_user_idx)
    return result

#3. Done 조회
def done(observed_user_idx=""):
    api = api_list.mytask_done
    result = wh_setting.get_requests(api=api,observed_user_idx = observed_user_idx)
    return result

#4. CC 목록 조회
def cc(last="",observed_user_idx=""):
    api = api_list.mytask_cc %(last)
    result = wh_setting.get_requests(api=api,observed_user_idx = observed_user_idx)
    return result