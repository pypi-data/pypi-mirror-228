# -*- coding: utf-8 -*-

from . import wh_setting, api_list

#WH2API - team.md

# 1. 팀 목록 조회
def list():
    api = api_list.team_list
    result = wh_setting.get_requests(api=api)
    return result

# 4. 팀 참여 가능한 이용자 목록 조회
def user_list(team_idx):
    api = api_list.team_user_list %(team_idx)
    result = wh_setting.get_requests(api=api)
    return result