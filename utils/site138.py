#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   site138.py
@Time    :   2019/11/13 23:05:59
@Author  :   shinpachi
@Version :   1.0
@Contact :   jiaxy0101@gmail.com
'''
import re
import json
import requests
import logging
from bs4 import BeautifulSoup as bs

def is_domain(domain):
    domain_regex = re.compile(
        r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z', 
        re.IGNORECASE)
    return True if domain_regex.match(domain) else False

class Site138(object):
    """docstring for Site138"""
    def __init__(self, domain):
        super(Site138, self).__init__()
        self.domain = domain
        self.subset = []
        self.website = "http://site.ip138.com/{}/domain.htm"

    def run(self):
        try:
            target = self.website.format(self.domain)

            response = requests.get(target)
            if response.status_code == 200:
                # print(response.status_code)
                soup = bs(response.text, 'lxml')
                div = soup.find_all('div', class_='panels')
                # print(div)
                if div:
                    for p in div[0].find_all('p'):
                        # print(p.text.strip())
                        sub = p.text.strip()
                        if is_domain(sub):
                            self.subset.append(sub)



            return list(set(self.subset))
        except Exception as e:
            # print(repr(e))
            logging.info(str(e))
            return self.subset

# passive = Site138('baidu.com')
# print(passive.run())