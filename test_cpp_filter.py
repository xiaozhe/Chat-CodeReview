# -*- coding: utf-8 -*-
# @Time    : 2024/03/13
# @Author  : dengss
# @Email   : xiaozhe@gmail.com


import os

from flask import Flask, jsonify, make_response

from app.chat import chat
#from app.git import git

from app.test_content_h_cpp import content_test
from app.test_content_h_cpp import lines_content_test


if __name__ == '__main__':
    #content_test()
    lines_content_test();
