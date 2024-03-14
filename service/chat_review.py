# -*- coding: utf-8 -*-
# @Time    : 2023/7/10 11:34
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : chat_review.py
# @Software: PyCharm
import os
import openai
import requests
from openai import OpenAIError
from retrying import retry

from config.config import gitlab_server_url, gitlab_private_token, openai_api_key, openai_baseurl, openai_model_name
from service.content_handle import filter_diff_content
from service.content_handle_cpp import filter_diff_content_cpp
from utils.LogHandler import log

"""
传入project_id和project_commit_id
ChatGPT代码补丁审查
"""

# 配置openai
openai_api_key = openai_api_key
gitlab_private_token = gitlab_private_token
gitlab_server_url = gitlab_server_url
headers = {
    "PRIVATE-TOKEN": gitlab_private_token,
}


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def post_comments(id, commit_id, content):
    data = {
        'note': content
    }
    comments_url = f'{gitlab_server_url}/api/v4/projects/{id}/repository/commits/{commit_id}/comments'
    response = requests.post(comments_url, headers=headers, json=data)
    log.debug(f"请求结果: {response.json}")
    if response.status_code == 201:
        comment_data = response.json()
        # 处理创建的评论数据
        log.info(f"创建评论成功，评论id: {comment_data}")
    else:
        log.error(f"请求失败，状态码: {response.status_code}")


def wait_and_retry(exception):
    return isinstance(exception, OpenAIError)


@retry(retry_on_exception=wait_and_retry, stop_max_attempt_number=3, wait_fixed=60000)
def generate_review_note(file_ext, change, project_id, branch_name, project_commit_id):
    new_path = change['new_path']
    change_diff = change['diff']
    # 仅对cpp、c文件进行review
    # if any(ext in file_ext for ext in ['.cpp', '.c']):
    if( file_ext in ['.c', '.cpp']):    
        content = filter_diff_content_cpp(change_diff, new_path, project_id, branch_name, project_commit_id)
    else:
        content = filter_diff_content(change['diff'])
        # content = ""
    if len(content) <= 0:
        review_note = f'### `{new_path}`' + '\n\n'
        review_note += f'\n\n未能提取提交内容**未提交到AI进行review**\n\n'
        log.info(f'对 {new_path} review结束')
        return review_note
    openai.api_key = openai_api_key
    openai.api_base = openai_baseurl
    messages = [
        {"role": "system",
         "content": "你是是一位资深编程专家，gitlab的commit代码变更将以git diff 字符串的形式提供，以格式「变更评分：实际的分数」给变更打分，分数区间为0~100分。输出格式：然后，以精炼的语言、严厉的语气指出存在的问题。如果你觉得必要的情况下，可直接给出修改后的内容。你的反馈内容必须使用严谨的markdown格式。"
         },
        {"role": "user",
         "content": f"请review这部分代码变更{content}",
         },
    ]
    response = openai.ChatCompletion.create(
        model=openai_model_name,
        messages=messages,
    )
    log.info(f'对 {new_path} review中...')
    response_content = response['choices'][0]['message']['content'].replace('\n\n', '\n')
    total_tokens = response['usage']['total_tokens']
    review_note = f'### `{new_path}`' + '\n\n'
    # review_note += f'diff:\n```\n{change_diff}\n```' + '\n\n'
    review_note += f'提交内容:\n```\n{content}\n```' + '\n\n'
    review_note += f'({total_tokens} tokens) {"AI review 意见如下:"}' + '\n\n'
    review_note += response_content
    log.info(f'对 {new_path} review结束')
    return review_note


def chat_review(project_id, branch_name, project_commit_id, content):
    log.info('开始code review')
    fileListNoReview=[]
    for change in content:
        ####log.info(f"单项目的commit内容： {change}")
        # 判断文件类型，只对py、java、class、vue文件进行review
        file_ext = os.path.splitext(change['new_path'])[1]
        #if any(ext in file_ext for ext in ['.py', '.java', '.class', '.vue', '.h', '.cpp', '.c']):
        #if any(ext in file_ext for ext in ['.h', '.cpp', '.c']):
        if( file_ext in ['.h', '.cpp', '.c']):
            try:
                review_note = generate_review_note(file_ext, change, project_id, branch_name, project_commit_id)
                log.info(f'对 {change["new_path"]}  , review结果如下：{review_note}')
                post_comments(project_id, project_commit_id, review_note)
            except Exception as e:
                log.error(f'出现异常，异常信息：{e}')
        else:
            fileListNoReview.append(change['new_path'])
            log.error(f'格式不正确，对 {change["new_path"]}  , 不需要review')

    if len(fileListNoReview) > 0:
        try:
            sFileList='\n\n'.join(fileListNoReview)
            post_comments(project_id, project_commit_id, f'### 以下文件**未提交到AI进行review**:\n\n' + sFileList)
        except Exception as e:
            log.error(f'出现异常，异常信息：{e}')
        #log.error(f'格式不正确，对 {fileListNoReview}  , 不需要review')


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def review_code(project_id, branch_name, project_commit_id):
    for commit_id in project_commit_id:
        url = f'{gitlab_server_url}/api/v4/projects/{project_id}/repository/commits/{commit_id}/diff'
        # log.info(f"开始请求gitlab的{url}   ,commit: {commit_id}的diff内容")

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.json()
            # 开始处理请求的类容
            #### log.info(f"开始处理All请求的类容: {content}")
            chat_review(project_id, branch_name, commit_id, content)
        else:
            log.error(f"请求gitlab的{url}commit失败，状态码：{response.status_code}")
            raise Exception(f"请求gitlab的{url}commit失败，状态码：{response.status_code}")

def test_review_code():
    project_id = 5
    project_commit_id = ['5147c49d897bdcb8d0edd6af8c782c360a0f15fa']
    version = "E312-dss-test-01"
    review_code(project_id, version, project_commit_id)
    
def test_review_code_2():
    project_id = 5
    project_commit_id = ['418ceb3d4c9cf9b99b6b72d3efc07291d01a687c']
    version = "E311-01-pbl--tb"
    review_code(project_id, version, project_commit_id)

if __name__ == '__main__':
    project_id = 787
    project_commit_id = ['ac98654c27a669bf88ce6d261d371a259c19dfcc']
    # os.environ["HTTP_PROXY"] = "http://192.168.96.19:7890"
    # os.environ["HTTPS_PROXY"] = "http://192.168.96.19:7890"
    log.info(f"项目id: {project_id}，commit_id: {project_commit_id} 开始进行ChatGPT代码补丁审查")
    review_code(project_id, project_commit_id)
    # post_comments(data)
