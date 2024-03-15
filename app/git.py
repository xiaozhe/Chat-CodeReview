# -*- coding: utf-8 -*-
# @Time    : 2023/7/7 21:22
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : git.py
# @Software: PyCharm
import json
from os import abort

from flask import Blueprint, request, jsonify

from config.config import WEBHOOK_VERIFY_TOKEN
from service.chat_review import review_code
from utils.LogHandler import log

import queue
import threading
import time
import signal
import sys

qCmmitList = queue.Queue(100)
#lockList = Lock.Lock()
semThread = threading.Condition()
iIsStopRun = 0
iIsEndedDeal = 0

git = Blueprint('git', __name__)
"""
git的蓝图

主要功能：获取gitlab的webhook，进行代码检查
"""



@git.route('/api')
def question():
    return 'hello world'


@git.route('/webhook', methods=['GET', 'POST'])
def webhook():
    global semThread
    global qCmmitList
    """
    gitlab的webhook,用来接受gitlab的推送
    http://192.168.96.19:5000/git/webhook
    """
    if request.method == 'GET':
        # 获取gitlab的webhook的token
        verify_token = request.headers.get('X-Gitlab-Token')

        # gitlab的webhook的token验证
        if verify_token == WEBHOOK_VERIFY_TOKEN:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'bad token'}), 401

    elif request.method == 'POST':
        """
        webhook的主要逻辑,获取gitlab的推送信息
        """
        # 获取gitlab的推送信息
        gitlab_message = request.data.decode('utf-8')
        # 将gitlab的推送信息转换为字典
        gitlab_message = json.loads(gitlab_message)
        # 获取项目的类型
        object_kind = gitlab_message.get('object_kind')
        # 获取gitlab的webhook的token
        verify_token = request.headers.get('X-Gitlab-Token')

        """
        项目为commit时，才进行代码检查，目前我只实现了commit的检查，后续可以添加merge和tag的检查
        
        涵盖push（commit）、merge（合并请求）和tag（标签创建）等三种代码提交方式
        """
        # 项目为commit时，才进行代码检查
        if verify_token == WEBHOOK_VERIFY_TOKEN and object_kind == 'push':
            # 验证通过，获取commit的信息
            print(gitlab_message)
            project_name = gitlab_message.get('project')['name']
            push_ref = gitlab_message.get('ref')

            # 获取项目id
            project_id = gitlab_message.get('project')['id']
            # 获取所有的commit的id
            project_commit_id = gitlab_message.get('commits')
            # 获取项目的分支
            version = gitlab_message.get('ref').split('/')[-1]
            # 定义一个空列表，用来存放commit的id
            commit_list = []
            # 定义一个空列表，用来存放commit的url
            commit_list_url = []

            # 遍历commit的id
            #for i in project_commit_id:
            #    commit_list.append(i['id'])
            #    commit_list_url.append(i['url'])
            last_commit_id=project_commit_id[0]['id']
            last_commit_url=project_commit_id[0]['url']
            for i in project_commit_id:
                last_commit_id = i['id']
                last_commit_url = i['url']
            commit_list.append(last_commit_id)
            commit_list_url.append(last_commit_url)

            # print(project_id, version, commit_list)
            #log.info(f"项目id: {project_id}，分支: {version}，commit_id: {commit_list} ")
            # 440 dev ['df4fa64a43f9b227c90d46a71556b717812635ca']
            log.info(f"项目id: {project_id}，分支: {version}，commit_url: {commit_list_url}")
            # print(commit_list_url)
            # ['https://gitlab.xxx.com/risk/xxx-risk-xxx/-/commit/df4fa64a43f9b227c90d46a71556b717812635ca']
            #
            # for i in commit_list:
            #     # 获取commit的变更文件
            #     web_url = f"{gitlab_server_url}/api/v4/projects/{project_id}/repository/commits/{i}/diff"
            #     print(web_url)
            # https://gitlab.xxx.com/api/v4/projects/440/repository/commits/df4fa64a43f9b227c90d46a71556b717812635ca/diff

            """
            总结：
            可用的参数：
            project_id 项目id   必须
            version 分支 
            commit_list commit的id   必须
            commit_list_url commit的url
            web_url commit的变更文件 
            """
            #log.info(f"项目id: {project_id}，commit_id: {commit_list} 开始进行ChatGPT代码补丁审查")
            #review_code(project_id, version, commit_list)
            
            itemCommit = [project_id, version, commit_list]
            semThread.acquire()
            qCmmitList.put(itemCommit)
            semThread.notify()
            semThread.release()

            return jsonify({'status': 'success'}), 200

        else:
            log.error("项目不是push")
            return jsonify({'status': 'bad token'}), 401

    else:
        abort(400)

def signal_handler(signum, frame):
    global iIsStopRun
    global iIsEndedDeal
    global semThread
    iIsStopRun = 1
    semThread.acquire()
    semThread.notify()
    semThread.release()
    while iIsEndedDeal != 1 :
        time.sleep(1)
        print("wait for deal end")
    print("exit......")
    sys.exit(0)

signal.signal(signal.SIGINT,signal_handler)

def thread_start():
    t_deal = threading.Thread(target=thread_run)
    t_deal.start()

def thread_run():
    global iIsStopRun
    global iIsEndedDeal
    global semThread
    global qCmmitList
    while True :
        semThread.acquire()
        semThread.wait()
        if iIsStopRun == 1 :
            semThread.release()
            iIsEndedDeal = 1
            break
        itemCommit=[]
        #lockList.lock()
        if not qCmmitList.empty():
            itemCommit=qCmmitList.get()
        #lockList.unlock()
        semThread.release()
        # log.info(f"get itemcommit len :" + str(len(itemCommit)))
        if len(itemCommit) > 0:
            project_id = itemCommit[0]
            version = itemCommit[1]
            commit_list = itemCommit[2]
            log.info(f"项目id: {project_id}，分支: {version}，commit_id: {commit_list} 开始进行ChatGPT代码补丁审查")
            review_code(project_id, version, commit_list)
