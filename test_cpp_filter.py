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

def test_filter_file_ext(_ext):
    file_ext=_ext
    if( file_ext in ['.h', '.c', '.cpp']):    
        print(file_ext + " file ext is in")
    else:
        print(file_ext + " file ext is not in")

if __name__ == '__main__':
    test_filter_file_ext(".c");
    test_filter_file_ext(".cpp");
    test_filter_file_ext(".h");
    test_filter_file_ext(".html");
    #content_test()
    #lines_content_test();
