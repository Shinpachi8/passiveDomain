#!/usr/bin/env python
# coding=utf-8

import os
import json
import time
import sys

FPATH = '/mnt/e/2 tools/5 dnsdata/fdns_a.sort.txt'
MAXLINESIZE = 500
WALKBYTES = 10000
LIMIT = {
    'MaxScan':   100,
    'MaxOutputLines': 100000
}


def get_string(f, offset):
    try:
        f.seek(offset, 0)
        line = f.read(MAXLINESIZE).split('\n')
        if len(line) < 2:
            return ''
        return line[1]
        print(line)
    except Exception as e:
        return ''


def get_line_detail(f, offset, search):
    line = get_string(f, offset)
    if line == '':
        return ''
    if len(line) > len(search):
        line = line[:len(search)]
    return line


def binary_search(f, left, filesize, search):

    right = filesize
    # 基本判断
    if right >= left:
        mid = int(left + (right - left) / 2)

        # 元素整好的中间位置
        line = get_line_detail(f, mid, search)
        # print(line)
        if line == search:
            return mid

        # 元素小于中间位置的元素，只需要再比较左边的元素
        elif line > search:
            # print('bigger')
            return binary_search(f, left, mid - 1, search)

        # 元素大于中间位置的元素，只需要再比较右边的元素
        else:
            # print('lower')
            return binary_search(f, mid + 1, right, search)

    else:
        # 不存在
        return -1


def get_all_match(f, offset, search):
     # back to search non match line
    max_scan = LIMIT['MaxScan']
    min_search_offset = offset
    search_length = len(search)
    all_line = []
    while True:
        if max_scan <= 0:
            break

        min_search_offset = offset - WALKBYTES
        if min_search_offset < 0:
            return []
        line = get_line_detail(f, min_search_offset, search)
        if line == '':
            return []
        if line != search:
            break
        max_scan -= 1

    f.seek(min_search_offset)

    max_output_line = LIMIT['MaxOutputLines']
    first_match = False
    while True:
        if max_output_line <= 0:
            break
        line = f.readline().strip()
        match_string = line[:len(search)] if len(
            line) > search_length else line
        if match_string == search:
            all_line.append(line)
            if first_match is False:
                first_match = True
        elif first_match:
            break
    return all_line


def search_rapid7(search):
    f = open(FPATH, 'r')
    fsize = os.path.getsize(FPATH)
    search = search[::-1]
    offset = binary_search(f, 0, fsize, search)
    all_line = get_all_match(f, offset, search)
    all_line = [i[::-1] for i in all_line]
    f.close()
    # print("total result:  {}".format(len(all_line)))
    # print(end - start)
    return all_line


if __name__ == '__main__':
    search_rapid7(".baidu.com")
