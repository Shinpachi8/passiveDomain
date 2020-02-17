#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   fetchDomainFromCrt.py
@Time    :   2019/11/13 23:05:59
@Author  :   shinpachi
@Version :   1.0
@Contact :   jiaxy0101@gmail.com
'''


import requests
import re
import sys
import tld
import time
from bs4 import BeautifulSoup as bs

from reverse_search import search_rapid7
from utils.site138 import Site138
from utils.sitecrt import GetDOmainBYCrt

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
    'AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/69.0.3497.100 Safari/537.36'
}
DNS_PATTERN = re.compile(r'DNS:(.*?)<BR>')
DNSBUFF = 'https://dns.bufferover.run/dns?q='


def is_ip(s):
    s = s.split('.')
    condition_a = len(s) == 4
    if condition_a is False:
        return False
    condition_b = [i.isdigit() and int(i) >= 0 and int(i) <= 255 for i in s]
    return all(condition_b)


def get_cdn_host():
    count = 0
    while count < 10:
        try:
            resp = requests.get('https://raw.githubusercontent.com/Shinpachi8/leetcode/master/algorithms/cdndomain.txt',
                                headers=HEADERS,)
            cdn_hosts = [i.strip() for i in resp.text.split("\n")]
            return set(cdn_hosts).difference(set([""]))
        except Exception as e:
            print(repr(e))
        count += 1
        time.sleep(5)

def main(domain, domain_out, ip_out):
    # crt获取域名1
    start = time.time()
    cdn_hosts = get_cdn_host()
    crt_obj = GetDOmainBYCrt(domain)
    crt_obj.run()
    crt_fld = crt_obj.all_fld_domain
    crt_domain = crt_obj.all_domain
    # crt_domain = set()
    # site 138获取域名
    cdn_list = set()
    results = set()
    ip_results = set()
    for fld in crt_fld:
        print(fld + ":\t")
        j = search_rapid7('.' + fld)
        ip_count, domain_count = 0, 0
        for i in j:
            try:
                ip, domain = i.split(',')[0].strip(), i.split(',')[1].strip()
                if is_ip(ip):
                    ip_results.add(ip)
                    ip_count += 1
                else:
                    if (ip.find('cdn') >= 0 and not ip.endswith(i)) or any([ip.find(k) >= 0 for k in cdn_hosts]):
                        # print(ip)
                        cdn_list.add(ip)
                    else:
                        results.add(ip)
                        domain_count += 1
                if any([domain.find(k) for k in cdn_hosts]):
                    continue
                results.add(domain)
                domain_count += 1
            except Exception as e:
                print(repr(e))
        obj_138 = Site138(fld)
        obj_138.run()
        obj_138_subset = set(obj_138.subset)
        results = results.union(obj_138_subset)
        print("\t\t  ip_count:{}\t\t domain_count:{}\t\t ip138_domain_count {}".format(ip_count, domain_count, len(obj_138_subset)))
    results = results.union(crt_domain)
    end = time.time()
    print("use:   {}".format(end - start))
    print("total:  {}".format(len(results)))
    print("cdn:  {}".format(len(cdn_list)))
    with open(ip_out, "w") as f:
        for i in ip_results:
            f.write(i + "\n")
    with open(domain_out, "w") as f:
        for i in results:
            f.write(i + "\n")

    with open("cdn_list.txt", "a") as f:
        for i in cdn_list:
            f.write(i + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:  python {} baidu.com domain_out.txt ip_out.txt".format(
            sys.argv[0]))
    target = sys.argv[1]
    domain_out = sys.argv[2]
    ip_out = sys.argv[3]
    main(target, domain_out, ip_out)
