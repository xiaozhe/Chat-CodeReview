# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 11:01
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : get_commit_content.py
# @Software: PyCharm

import os
import re
import requests

from service.get_url_raw import get_gitlab_file_content
#from config.apollo_config import gitlab_server_url, gitlab_private_token
from config.config import gitlab_server_url, gitlab_private_token
# from service.call_java_json import process_java_file
#from service.content_handle_cpp import get_node_by_lines_and_content
from utils.LogHandler import log

"""
获取Gitlab项目中commit_id的文件，然后调用call_java_json.py中的process_java_file函数处理
传入参数：
project_id：项目ID
version：分支或标签
commit_id：commit_id
"""

def get_commit_diff_add_lines(contentDiff) :
    reg = re.compile("^@@ -[0-9]+(,[0-9]+)? \+([0-9]+)(,[0-9]+)? @@")
    diffLines=contentDiff.split('\n')                    

    iChangedLineValue=0
    iIndexLineDiffInfo=0
    iIndexLine=0
    bIsLineDiff=False
    bIsLineAdd=False
    bIsLineRemove=False
    iContRemoveLine=0
    linesRet=[]
    for line in diffLines:
        iIndexLine+=1
        diffInfo=reg.findall(line)
        bIsLineDiff=False        
        if len(diffInfo) > 0:
            iChangedLineValue = int(diffInfo[0][1])
            iIndexLineDiffInfo=iIndexLine
            bIsLineDiff=True
            iContRemoveLine=0
        if bIsLineDiff :
            #sDiffInfo="diffInfo len: " + str(len(diffInfo)) + " " + "iIndexLine: " + str(iIndexLine)
            #for i1 in diffInfo:
            #    sDiffInfo = sDiffInfo + str(i1) + " "
            #print (sDiffInfo)
            #print (str(iChangedLineValue) + " " + str(iIndexLineDiffInfo) + " >>>###>>> " + line)
            continue
        
        bIsLineAdd=False
        bIsLineRemove=False
        if len(line) > 0:
            if line[0] == '+':
                bIsLineAdd=True
            if line[0] == '-':
                bIsLineRemove=True
        if bIsLineRemove :
            iContRemoveLine+=1
        if bIsLineAdd :
            iNumDiffLine=iIndexLine-iIndexLineDiffInfo-iContRemoveLine-1
            iNumFillLine=iChangedLineValue+iNumDiffLine
            linesRet.append((iNumFillLine, line))
            ### iNumDiffLine.>> 从diff信息行到当前行的行数.. iIndexLine >> diff内容的当前行值...iIndexLineDiffInfo >> diff信息行行值...iContRemoveLine >> 从信息行开始的删除行数...
            #print(">>>>>> " + str(iNumDiffLine) + " = " + str(iIndexLine) + " - " +str(iIndexLineDiffInfo) + " - " + str(iContRemoveLine) + " -1 ")
            ### iNumFillLine 添加行的行值...iChangedLineValue >> diff信息记录的行号...iNumDiffLine >> 从diff信息行到当前行的行数...
            #print(" >>>>> " + str(iNumFillLine) + " = " +str(iChangedLineValue) + " + " + str(iNumDiffLine) + "   >>>> " + line)
    return linesRet

def get_commit_content_test(project_id, version, commit_id):
    headers = {
        "PRIVATE-TOKEN": gitlab_private_token,
    }
    if commit_id:
        for commit in commit_id:
            log.info(f"开始获取commit_id的路径: {commit}")
            file_dir = []
            url = f'{gitlab_server_url}/api/v4/projects/{project_id}/repository/commits/{commit}/diff'
            log.info(f"{commit}  开始请求gitlab的 {url} ，commit: {commit_id}的路径")
            response = requests.get(url, headers=headers)
            if response.status_code == 200:

                content = response.json()
                ## print(content)
                ## return [];
                # 开始处理请求的内容
                # log.info(f"开始处理请求的内容: {content}")
                iIndexFile=0
                for i in content:
                    iIndexFile+=1                    
                    file_path=i['new_path']
                    file_ext = os.path.splitext(file_path)[1]
                    print(file_ext + "         " + file_path)
                    isCfile=any(ext in file_ext for ext in ['.h','.cpp', '.c'])
                    isCppfile=any(ext in file_ext for ext in ['.cpp', '.c'])
                    if isCppfile :
                        fileContent=get_gitlab_file_content(project_id, file_path, version)
                        # print(fileContent)
                        # 保存fileContent到文件
                        # file_path="./json_test_view/100" + str(iIndexFile) + ".json"
                        # with open(file_path, 'w') as f:
                        #      f.write(fileContent)

                        # file_path="./json_test_view/200" + str(iIndexFile) + ".json"
                        # with open(file_path, 'w') as f:
                        #     f.write(i['diff'])
                    
                        linesChange = get_commit_diff_add_lines(i['diff'])
                        if( len(linesChange) > 0 ):
                            #for lineAdd in linesChange:
                            #    print(lineAdd)
                            #listNodes = get_node_by_lines_and_content(linesChange, fileContent)
                            listNodes = [];
                            print("===================================================================")
                            print( "listNodes count: " + str(len(listNodes)))
                            for node in listNodes:
                                print("           -----------------------------------------------------")
                                print( node.text.decode() )
                                print("           -----------------------------------------------------")
                            print("===================================================================")

                    print(file_path)

                    if any(ext in i['new_path'] for ext in ['.py', '.java', '.class', '.vue', '.h', '.cpp', '.c']):
                        print("check ext true")
                    else :
                        print("check ext false")
                    # file_dir.append(i['new_path'])
                    # process_java_file(project_id, i['new_path'], version)
                log.info(f"数量： {len(file_dir)}  获取到的文件路径: {file_dir}")
    else:
        return []

def test_get_commit():
    # 测试取得commit 内容
    project_id = 5
    # version = "E311-01-pbl--tb"
    # commit_id = ['b2a22a25650cb07cf132f1be14109a9ca791ae5f']
    # version = "E308-dss-test-01--01"
    # commit_id = ['9b61411719ca3db42c9e788d9e69f01a2a24cf13']
    version = "E308-02-pbl--tb"
    commit_id = ['418ceb3d4c9cf9b99b6b72d3efc07291d01a687c']

    file_dir = get_commit_content_test(project_id, version, commit_id)

def test_get_commit_file():
    # 测试取得分支文件内容
    project_id = 5
    file_path = 'yml_gitlab_tools/auto_create/build_machine_tags_release.txt'
    version = "E311-01-pbl--tb"
    file_content = get_gitlab_file_content(project_id, file_path, version)
    print(file_content)


if __name__ == "__main__":
    # 调用函数示例
    project_id = 798
    version = "dev"
    commit_id = ['d8f3dda9b233224edcd61c46f97391fb3b53dd42']

    file_dir = get_commit_content_test(project_id, version, commit_id)
