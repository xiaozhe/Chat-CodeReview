# -*- coding: utf-8 -*-
# @Time    : 2024/03/13
# @Author  : dengss
# @Email   : xiaozhe@gmail.com


import os

from flask import Flask, jsonify, make_response

from app.chat import chat
#from app.git import git
from utils.LogHandler import log

from config.config import WEBHOOK_VERIFY_TOKEN
#from service.get_commit_content import test_get_commit
#from service.get_commit_content import test_get_commit_file

from service.chat_review import test_review_code
#from service.chat_review_debug import test_review_code


if __name__ == '__main__':
    test_review_code()
    # test_get_commit_file();
