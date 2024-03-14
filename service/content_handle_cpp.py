# -*- coding: utf-8 -*-
# @Time    : 2024/03/13
# @Author  : dengss
# @Email   : xiaozhe@gmail.com
# @File    : content_handle_cpp.py


from tree_sitter import Language, Parser
from service.get_commit_content import get_commit_diff_add_lines
from service.get_url_raw import get_gitlab_file_content

# 注意C++对应cpp，C#对应c_sharp（！这里短横线变成了下划线）
# 看仓库名称
# CPP_LANGUAGE = Language('../tree-sitter-build/my-languages.so', 'cpp')
# CPP_LANGUAGE = Language('tree-sitter-build/my-languages.so', 'cpp')
CPP_LANGUAGE = Language('/usr/lib/my-languages.so', 'cpp')
#CS_LANGUAGE = Language('build/my-languages.so', 'c_sharp')

# 举一个CPP例子
cpp_parser = Parser()
cpp_parser.set_language(CPP_LANGUAGE)

def traverse_node_children(_node, _level=0):
    countN = len(_node.children)
    sLevelSpace = "  " * _level + " L: " + str(_level) + " "
    # print( sLevelSpace + "level " + str(_level) )
    # print( sLevelSpace + "node " + _node.type + _node.text ) # text is bytes.....
    # print( sLevelSpace + " " + _node.type + _node.text.decode() )
    # print( _node )
    if countN > 0:
        for j in range(countN):
            nodeChild=_node.children[j]
            traverse_node_children(nodeChild, _level + 1)
    

def get_node_by_line_num_traverse(_declaration, _function, __node, _line_num, _level=0):
    countN = len(__node.children)
    if __node.start_point[0] > _line_num :
        ## print( "================================================" )
        ## print( __node )
        return
    while True:
        if __node.start_point[0] > _line_num :
            # 开始行数比检查行大，退出
            break;
        if __node.end_point[1] == 0 and __node.end_point[0] == _line_num :
            break;
        if __node.end_point[0] < _line_num :
            # 结束行数比检查行小，退出
            break;
        #if __node.type in ["preproc_include", "function_definition", "declaration"]:
        #    print(__node.type + "type in list ...")
        #else:
        #    print(__node.type + "type not in list ...")
        
        if __node.type == "function_definition" :
            _function.append(__node);
            #print( __node )
            #break;
        if __node.type in ["preproc_include", "preproc_def", "declaration"]:
            _declaration.append(__node);
            #print(" ================line : " + str(_line_num) + " ================")
            #print( __node )
            #print( __node.text.decode() )
            #break;
        #sLevelSpace = "  " * _level + " L: " + str(_level) + " "
        ## print( "------------------------------------------------" )
        #print( sLevelSpace + "start--end " + str(__node.start_point[0]) + "--" + str(__node.end_point[0]) + " " + __node.type)
        ## # print( sLevelSpace + "node " + __node.type + __node.text ) # text is bytes.....
        ## print( __node.text.decode() )
        ## print( "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" )
        ## # print( __node )
        ## # return __node
        break;
    if __node.start_point[0] == __node.end_point[0] and __node.start_point[0] == _line_num :
        # print( "================================================" )
        # print( __node )
        # print( __node.text.decode() )
        # print( "================================================" )
        return;
    if countN <= 0:
        return;
    for j in range(countN):
        nodeChild= __node.children[j]
        if nodeChild.start_point[0] > _line_num :
            break
        get_node_by_line_num_traverse(_declaration, _function, nodeChild, _line_num, _level + 1)
    return;

def get_node_by_line_num(_ret_nodes, _node, _line_num):
    list_declaration = []
    list_function = []
    list_declaration.clear()
    list_function.clear()
    #print( "-------------------------tree-detter-line num : " + str(_line_num) + "--------------------------")
    get_node_by_line_num_traverse(list_declaration, list_function, _node, _line_num, 0)
    if len(list_function) > 0 :
        _ret_nodes.append(list_function[0])
    elif len(list_declaration) > 0 :
        _ret_nodes.append(list_declaration[0])

    ## if len(list_declaration) > 0 :
    ##     # print node_declaration
    ##     node_declaration = list_declaration[0]
    ##     print( "----node declaration--------------------------------------------" )
    ##     print( "start--end " + str(node_declaration.start_point[0]) + "--" + str(node_declaration.end_point[0]) + " " + node_declaration.type)
    ##     # print( sLevelSpace + "node " + _node.type + _node.text ) # text is bytes.....
    ##     print( node_declaration.text.decode() )
    ##     print( "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" )
    ##     _ret_nodes.append(node_declaration)
    ## else :
    ##     print( "----no declaration node--------------------------------------------" )
    ## 
    ## if len(list_function) > 0 :
    ##     # print node_function
    ##     node_function = list_function[0]
    ##     print( "----node function--------------------------------------------" )
    ##     print( "start--end " + str(node_function.start_point[0]) + "--" + str(node_function.end_point[0]) + " " + node_function.type)
    ##     # print( sLevelSpace + "node " + _node.type + _node.text ) # text is bytes.....
    ##     print( node_function.text.decode() )
    ##     print( "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" )
    ##     _ret_nodes.append(node_function)
    ## else :
    ##     print( "----no function node--------------------------------------------" )


def get_node_from_content_and_line_num(_content, _line_num):
    tree = cpp_parser.parse(bytes(_content, "utf8"))
    # 注意，root_node 才是可遍历的树节点
    root_node = tree.root_node
    list_nodes = []
    get_node_by_line_num(list_nodes, root_node, _line_num)
    return list_nodes;


def get_node_by_lines_and_content(_lines, _content):
    tree = cpp_parser.parse(bytes(_content, "utf8"))
    # 注意，root_node 才是可遍历的树节点
    root_node = tree.root_node
    list_nodes = []
    for lineAdd in _lines:
        isInListNode = False
        iLineNum=lineAdd[0]-1
        for node in list_nodes:
            iEndNode=node.end_point[0]
            if node.end_point[1] == 0 :
                iEndNode -= 1
            if iLineNum < node.start_point[0] : 
                continue
            if iLineNum > iEndNode : 
                continue
            isInListNode = True
            break
        #print( "get node from line: " + str(iLineNum+1) + " tree-sitter-行号: " + str(iLineNum) + " " + str(isInListNode) )
        if not isInListNode:
            # print("iLineNum = " + str(iLineNum))
            get_node_by_line_num(list_nodes, root_node, iLineNum)
    # print( "list_nodes len: " + str(len(list_nodes)) )
    return list_nodes;

def filter_diff_content_cpp(_diff, _path, project_id, branch_name, project_commit_id):
    linesChange = get_commit_diff_add_lines(_diff)
    if( len(linesChange) <= 0 ):
        return ""
    #print("================get lines=================")
    #for lineChg in linesChange:
    #    sLine=str(lineChg[0])+"   "+str(lineChg[1])
    #    print(sLine)
    #print("==========================================")

    fileContent=get_gitlab_file_content(project_id, _path, branch_name)
    # 保存fileContent到文件
    #with open('./files_save_test/fileContent.cpp', 'w') as f:
    #     f.write(fileContent)
    #     f.close()

    list_nodes = get_node_by_lines_and_content(linesChange, fileContent)
    if(len(list_nodes) <= 0):
        return ""
    
    contents = "";
    for node in list_nodes:
        contents = contents + '\n' + node.text.decode()
    return contents

if __name__ == '__main__':
    # 这是b站网友写的代码，解析看看
    cpp_code_snippet = '''
    namespace A1O {
    namespace A2O {
        

    static int g_a = 0;

    int mian{
    piantf("hell world 111");
    remake O;
    }

    int mian1{
    piantf("hell world 222");
    remake O;
    }

    }}
    '''

    # 没报错就是成功
    tree = cpp_parser.parse(bytes(cpp_code_snippet, "utf8"))
    # 注意，root_node 才是可遍历的树节点
    root_node = tree.root_node

    # 遍历root_node的例子
    # traverse_node_children(root_node)

    ## 测试 static int g_a = 0;
    get_node_by_line_num(root_node, 5) 

    ## 测试 int mian{
    #get_node_by_line_num(root_node, 7) 

    ## 测试 int mian{
    #get_node_by_line_num(root_node, 8) 

    ## 测试 }
    get_node_by_line_num(root_node, 10)
