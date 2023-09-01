# -*- coding: utf-8 -*-


from .. import wh
from . import wh_setting, api_list


#WH2API - episode.md

#1. 에피소드 목록 조회
def list(project_idx):
    api = api_list.episode_list %(project_idx)
    result = wh_setting.get_requests(api=api)
    return result

#2. 에피소드 등록
def create(project_idx,episode_name,description=""):
    api = api_list.episode_create %(project_idx)
    data = {"episode_name":episode_name,"description":description}
    result = wh_setting.post_requests(api=api, data=data)
    return result