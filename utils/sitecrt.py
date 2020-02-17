#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# Created on 11 月-24-19 11:18
# sitecrt.py
# @author: shinpachi
'''

import requests
import re
import sys
from bs4 import BeautifulSoup as bs
import tld
import time
import random
from multiprocessing.pool import Pool


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

def get_domain_from_crt_by_id(id):
    url = 'https://crt.sh/?id={}'.format(id)
    try:
        time.sleep(random.randint(2,7))
        resp = requests.get(url, headers=HEADERS, verify=False, timeout=30)
        # print(resp.content)
        all_sub = (DNS_PATTERN.findall(resp.text))
        return all_sub
    except Exception as e:
        return []

class GetDOmainBYCrt(object):

    def __init__(self, domain):
        self.domain = domain if domain.startswith('%.') else '%.' + domain

        self.all_fld_domain = set()
        self.all_domain = set()

    def get_all_ids(self):
        url = 'https://crt.sh/?q={}'.format(self.domain)
        resp = requests.get(url,
                            headers=HEADERS,
                            verify=False
                            )
        html = resp.content
        ids = []
        soup = bs(html, 'html.parser')
        tds = soup.find_all('td')
        for t in tds:
            if t.find('a'):
                i = t.find('a').text
                if i.isdigit():
                    ids.append(i)
            else:
                continue
        return list(set(ids))

    def get_domain_from_id(self, id):
        url = 'https://crt.sh/?id={}'.format(id)
        try:
            resp = requests.get(url, headers=HEADERS, verify=False)
            # print(resp.content)
            all_sub = (DNS_PATTERN.findall(resp.text))
            for i in all_sub:
                self.all_domain.add(i.replace("*.", ""))
            return all_sub
        except Exception as e:
            return []

    def get_fld_domain(self, domain=None):
        if domain is None:
            domain = self.domain
        try:
            fld = tld.get_fld(domain, fix_protocol=True)
            self.all_fld_domain.add(fld)
        except Exception as e:
            print(repr(e))
        # print(fld)

    def run(self):
        ids = self.get_all_ids()
        p = Pool(10)
        result = p.map(get_domain_from_crt_by_id, ids)
        for r1 in result:
            for r2 in r1:
                self.all_domain.add(r2.replace("*.", ""))

        for domain in self.all_domain:
            self.get_fld_domain(domain)

        return (self.all_fld_domain, self.all_domain)

def fetch_domain_from_crt(domain):
    crt = GetDOmainBYCrt(domain)
    ids = crt.get_all_ids()
    for i in ids:
        crt.get_domain_from_id(i)

    for domain in crt.all_domain:
        crt.get_fld_domain(domain)

    return (crt.all_fld_domain, crt.all_domain)