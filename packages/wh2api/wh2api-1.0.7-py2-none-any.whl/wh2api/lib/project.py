# -*- coding: utf-8 -*-

from . import wh_setting, api_list

#WH2API - project.md

#1. 프로젝트 목록 조회
def list(finished=""):
    # finished = '1' 끝난 프로젝트도 조회
    api = api_list.project_list
    data = {"including_finished": finished, "all": "1"}
    result = wh_setting.get_requests(api=api,data=data)
    return result

#2. 프로젝트 상세 정보 조회
def read(project_idx):
    api = api_list.project_read %(project_idx)
    result = wh_setting.get_requests(api=api)
    return result