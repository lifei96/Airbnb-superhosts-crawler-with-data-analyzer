# -*- coding: utf-8 -*-

import urllib
import re
import os
import random
import time
from selenium import webdriver
from urllib import FancyURLopener
from random import choice


user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]


class MyOpener(FancyURLopener, object):
    version = choice(user_agents)


failed_list = list()


def mark_failed(uid):
    failed_list.append(uid)


def get_photo(uid):
    driver = webdriver.Firefox()
    time.sleep(random.randint(16, 20))
    url = 'https://www.airbnb.com/users/show/' + uid + '?locale=en'
    try:
        driver.get(url)
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        mark_failed(uid)
        print('-----marked')
        driver.quit()
        return
    try:
        photo_url = driver.find_element_by_class_name("img-responsive").get_attribute("src")
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        print('-----fail to get photo_url')
        driver.quit()
        return
    print(photo_url)
    time.sleep(random.randint(6, 10))
    opener = MyOpener()
    opener.retrieve(photo_url, './Data/Host/Photos/' + uid + '.jpg')
    driver.quit()


def crawl():
    with open('./Data/Host/host_sample_list.txt', 'r') as f:
        host_list = f.read().split('\n')
    random.shuffle(host_list)
    count = 0
    for uid in host_list:
        count += 1
        if count % 20 == 0:
            time.sleep(random.randint(150, 200))
        print(count)
        print(uid)
        if os.path.exists('./Data/Host/Photos/' + uid + '.jpg'):
            print('-----exists')
            continue
        try:
            get_photo(uid)
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print('-----failed')


if __name__ == '__main__':
    if not os.path.exists('./Data/Host/Photos'):
        os.mkdir('./Data/Host/Photos')
    crawl()
    with open('./Data/Host/photo_failed_list.txt', 'w') as out:
        out.write("\n".join(failed_list))
