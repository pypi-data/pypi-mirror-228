# -*- coding: utf-8 -*-

from . import wh_setting, api_list

#WH2API - asset-category.md

#1. 에셋 카테고리 목록 조회
def list(project_idx):
    api = api_list.category_list %(project_idx)
    result = wh_setting.get_requests(api=api)
    return result

#2. 에셋 카테고리 생성
def create(project_idx,category_name,description=""):
    api = api_list.category_create %(project_idx)
    data = {"category_name":category_name,"description":description}
    result = wh_setting.post_requests(api=api, data=data)
    return result