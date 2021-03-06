# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import os
import random
import time


user_agent_list = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
                   'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/55.0.2883.87 Chrome/55.0.2883.87 Safari/537.36',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                   'Mozilla/5.0 (X11; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36',
                   'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:50.0) Gecko/20100101 Firefox/50.0']


def read_profile():
    file_in = open('./Data/Superhost/Profile_Super.txt')
    superhost_list_tmp = file_in.read().split('\n')
    superhost_list = []
    for superhost in superhost_list_tmp:
        if superhost != '':
            superhost_list.append(superhost.split('\t'))
    return superhost_list


failed_list = list()


def mark_failed(uid):
    failed_list.append(uid)


def get_name(uid):
    url = 'https://www.airbnb.com/users/show/' + uid + '?locale=en'
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/50.0.2661.102 Safari/537.36')
    try:
        response = opener.open(req, timeout=10)
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        print('-----fail to get name data')
        return ''
    data = response.read()
    name = re.findall('Hey, I’m (.*?)!', data)
    if len(name):
        return name[0]
    else:
        return ''


def get_photo(uid):
    url = 'https://www.airbnb.com/users/show/' + uid + '?locale=en'
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    user_agent = user_agent_list[random.randint(0, len(user_agent_list) - 1)]
    req.add_header("User-agent", user_agent)
    try:
        response = opener.open(req, timeout=10)
    except urllib2.HTTPError, e:
        print(e.code)
        print('-----fail to get data')
        if e.code != 404:
            mark_failed(uid)
            print('-----marked')
        return
    data = response.read()
    photo_url = re.findall('" class="img-responsive" height="225" src="(.*?)" title="', data)
    if not photo_url:
        print('-----fail to get photo_url')
        mark_failed(uid)
        return
    photo_url = photo_url[0]
    print(photo_url)
    time.sleep(random.randint(5, 8))
    urllib.URLopener.version = user_agent
    urllib.urlretrieve(photo_url, './Data/Superhost/Photos/' + uid + '.jpg')


def crawl():
    with open('photo_failed_list.txt', 'r') as f:
        superhost_list = f.read().split('\n')
    random.shuffle(superhost_list)
    count = 0
    for uid in superhost_list:
        count += 1
        print(count)
        if count % 20 == 0:
            time.sleep(random.randint(30, 40))
        print(uid)
        if os.path.exists('./Data/Superhost/Photos/' + uid + '.jpg'):
            print('-----exists')
            continue
        try:
            # time.sleep(random.randint(4, 6))
            # name = get_name(uid)
            # if name == '':
            #     print('-----failed to get name')
            #     name = superhost[1]
            # print(name)
            time.sleep(random.randint(5, 8))
            get_photo(uid)
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print('-----failed')


if __name__ == '__main__':
    if not os.path.exists('./Data/Superhost/Photos'):
        os.mkdir('./Data/Superhost/Photos')
    crawl()
    with open('photo_failed_list.txt', 'w') as out:
        out.write("\n".join(failed_list))
