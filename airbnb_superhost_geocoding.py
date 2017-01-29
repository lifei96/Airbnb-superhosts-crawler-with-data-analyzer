# -*- coding: utf-8 -*-

import geocoder
import json
import os
import random


def read_profile():
    file_in = open('./Data/Superhost/Profile_Super.txt')
    superhost_list_tmp = file_in.read().split('\n')
    superhost_list = []
    for superhost in superhost_list_tmp:
        if superhost != '':
            superhost_list.append(superhost.split('\t'))
    return superhost_list


def get_location():
    with open('./geocoding_key.txt', 'r') as f:
        Keys = f.read().split('\n')
    while '' in Keys:
        Keys.remove('')
    superhost_list = read_profile()
    for superhost in superhost_list:
        user_id = superhost[0]
        print(user_id)
        address = superhost[2]
        print(address)
        if os.path.exists('./Data/Superhost/Location/' + user_id + '.json'):
            print('exists!')
            continue
        num = random.randint(0, len(Keys) - 1)
        try:
            geo = geocoder.google(address, key=Keys[num])
        except:
            del Keys[num]
            print('failed!')
            continue
        print(geo.json['status'])
        if geo.json['status'] != "OK":
            print('failed!')
            continue
        with open('./Data/Superhost/Location/' + user_id + '.json', 'w') as f:
            json.dump(geo.json, f, indent=4)


if __name__ == '__main__':
    if not os.path.exists('./Data/Superhost/Location'):
        os.mkdir('./Data/Superhost/Location')
    get_location()
