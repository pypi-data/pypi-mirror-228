# -*- coding: utf-8 -*-

from . import wh_setting, api_list

#WH2API - org.md


#1. 회사/조직 정보 조회
def read(org_id="std"):
    api = api_list.org_read %(org_id)
    result = wh_setting.get_requests(api=api)
    return result