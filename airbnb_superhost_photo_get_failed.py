# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import os
import random
import time


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


def crawl():
    superhost_list = read_profile()
    count = 0
    for superhost in superhost_list:
        count += 1
        print(count)
        uid = superhost[0]
        print(uid)
        if os.path.exists('./Data/Superhost/Photos/' + uid + '.jpg'):
            print('-----exists')
            continue
        mark_failed(uid)


if __name__ == '__main__':
    if not os.path.exists('./Data/Superhost/Photos'):
        os.mkdir('./Data/Superhost/Photos')
    crawl()
    random.shuffle(failed_list)
    with open('photo_failed_list.txt', 'w') as out:
        out.write("\n".join(failed_list))
