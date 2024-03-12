# -*- coding: utf-8 -*-
# @Time    : 2024/03/13
# @Author  : dengss
# @Email   : xiaozhe@gmail.com

import os

from service.content_handle_cpp import get_node_from_content_and_line_num
from service.content_handle_cpp import get_node_by_lines_and_content

def print_nodes(_list_nodes):
    countN = len(_list_nodes)
    for i in range(countN):
        node_print = _list_nodes[i]
        print( "----node--------------------------------------------" )
        sNodePos="node type: " + node_print.type
        sNodePos+="start--end "
        sNodePos+="(" + str(node_print.start_point[0]) + "--" + str(node_print.start_point[1]) + ")"
        sNodePos+=" ---- "
        sNodePos+="(" + str(node_print.end_point[0]) + "--" + str(node_print.end_point[1]) + ")"
        print(sNodePos)
        #print( "start--end " + str(node_print.start_point[0]) + "--" + str(node_print.end_point[0]) + " " + node_print.type)
        print( node_print.text.decode() )
        print( "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" )


def lines_content_test():
    cpp_code_snippet = '''
#define ICMP_DATA_LEN 56
#define ICMP_HEAD_LEN 8
#define ICMP_LEN  (ICMP_DATA_LEN + ICMP_HEAD_LEN)
u_int16_t Tools_Network::icmp_computer_cknum(char *_icmp)
{
    u_int16_t *data = (u_int16_t *)_icmp;
    int len = ICMP_LEN;
    u_int32_t sum = 0;

    while (len > 1) {
        sum += *data++;
        len -= 2;
    }
    if (1 == len) {
        u_int16_t tmp = *data;
        tmp &= 0xff00;
        sum += tmp;
    }
    while (sum >> 16){
        sum = (sum >> 16) + (sum & 0x0000ffff);
    }
    sum = ~sum;

    return sum;
}
'''
    lines = [];
    lines.append((1, ""));
    lines.append((2, ""));
    lines.append((3, ""));

    list_nodes = get_node_by_lines_and_content(lines, cpp_code_snippet)
    print_nodes(list_nodes)

    contents = "";
    for node in list_nodes:
        contents = contents + '\n' + node.text.decode()
    print("==============================code===========================") 
    print(contents) # contents

    #list_nodes = get_node_from_content_and_line_num(cpp_code_snippet, 1)
    #print_nodes(list_nodes)

    #list_nodes = get_node_from_content_and_line_num(cpp_code_snippet, 2)
    #print_nodes(list_nodes)

    #list_nodes = get_node_from_content_and_line_num(cpp_code_snippet, 8)
    #print_nodes(list_nodes)
#
    #list_nodes = get_node_from_content_and_line_num(cpp_code_snippet, 10)
    #print_nodes(list_nodes)



def content_test():
    cpp_code_snippet = '''
#define ICMP_DATA_LEN 56
#define ICMP_HEAD_LEN 8
#define ICMP_LEN  (ICMP_DATA_LEN + ICMP_HEAD_LEN)
u_int16_t Tools_Network::icmp_computer_cknum(char *_icmp)
{
    u_int16_t *data = (u_int16_t *)_icmp;
    int len = ICMP_LEN;
    u_int32_t sum = 0;

    while (len > 1) {
        sum += *data++;
        len -= 2;
    }
    if (1 == len) {
        u_int16_t tmp = *data;
        tmp &= 0xff00;
        sum += tmp;
    }
    while (sum >> 16){
        sum = (sum >> 16) + (sum & 0x0000ffff);
    }
    sum = ~sum;

    return sum;
}
'''
    #list_nodes = get_node_from_content_and_line_num(cpp_code_snippet, 1)
    #print_nodes(list_nodes)

    list_nodes = get_node_from_content_and_line_num(cpp_code_snippet, 2)
    print_nodes(list_nodes)

    #list_nodes = get_node_from_content_and_line_num(cpp_code_snippet, 8)
    #print_nodes(list_nodes)
#
    #list_nodes = get_node_from_content_and_line_num(cpp_code_snippet, 10)
    #print_nodes(list_nodes)


def content_test_1():
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
    ## 测试 static int g_a = 0;
    list_nodes = get_node_from_content_and_line_num(cpp_code_snippet, 5)
    print_nodes(list_nodes)

    ## 测试 int mian{
    list_nodes = get_node_from_content_and_line_num(cpp_code_snippet, 7)
    print_nodes(list_nodes)
    #get_node_by_line_num(root_node, 7) 

    ## 测试 int mian{
    list_nodes = get_node_from_content_and_line_num(cpp_code_snippet, 8)
    print_nodes(list_nodes)
    #get_node_by_line_num(root_node, 8) 

    ## 测试 }
    list_nodes = get_node_from_content_and_line_num(cpp_code_snippet, 10)
    print_nodes(list_nodes)
    #get_node_by_line_num(root_node, 10)

if __name__ == '__main__':
    content_test()
    

