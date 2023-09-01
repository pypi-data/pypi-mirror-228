# -*- coding: utf-8 -*-

from . import wh_setting, api_list

#WH2API - task.md

#14. 에셋 태스크 조회
def read(task_idx):
    api = api_list.asset_task_read %(task_idx)
    result = wh_setting.get_requests(api=api)
    return result

#12. 에셋 태스크 목록 조회
def list(project_idx,asset_idx):
    api = api_list.asset_task_list %(project_idx,asset_idx)
    result = wh_setting.get_requests(api=api)
    return result

#1. 에셋 태스크 벌크 등록(단일 사용)
def create(project_idx,asset_idx,tasktype_name):
    api = api_list.asset_task_create %(project_idx)

    #Task를 한개씩 등록 하는 경우 리스트로 반환
    asset_idx = list(str(asset_idx))
    tasktype_name = list(tasktype_name)

    data = {"asset_idx[]":asset_idx,"tasktype_name[]":tasktype_name}
    result = wh_setting.post_requests(api=api, data=data)
    return result


#1. 에셋 태스크 벌크 등록
def bulk_create(project_idx,asset_idx=[],tasktype_name=[]):
    api = api_list.asset_task_create %(project_idx)
    if len(asset_idx) == len(tasktype_name):
        data = {"asset_idx[]": asset_idx, "tasktype_name[]": tasktype_name}
        result = wh_setting.post_requests(api=api, data=data)
        return result
    else:
        print("not match count of asset_idx to tasktype_name")
        return None

#1. 에셋 태스크 벌크 등록 -- deprecate
def bulk_creaste(project_idx,asset_idx=[],tasktype_name=[]):
    print('this function is deprecated.')
    print('please, use \"bulk_create()\"')
    return bulk_create(project_idx, asset_idx, tasktype_name)


#7. 에셋 태스크 상태 코드 수정
def status_change(project_idx,task_idx,status_idx):
    api = api_list.asset_task_status_change %(project_idx,task_idx)
    data = {"status_idx":status_idx}
    result = wh_setting.post_requests(api=api, data=data)
    return result

#8. 에셋 태스크 업무 시작
def start(project_idx,task_idx):
    api = api_list.asset_task_start %(project_idx,task_idx)
    result = wh_setting.post_requests(api=api)
    return result

#9. 에셋 태스크 업무 시작
def stop(project_idx,task_idx):
    api = api_list.asset_task_stop %(project_idx,task_idx)
    result = wh_setting.post_requests(api=api)
    return result

