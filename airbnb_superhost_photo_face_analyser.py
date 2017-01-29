# -*- coding: utf-8 -*-

import os
import json
from get_face_info import get_face_info


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


def face_analyse():
    superhost_list = read_profile()
    count = 0
    for superhost in superhost_list:
        count += 1
        print(count)
        uid = superhost[0]
        print(uid)
        if os.path.exists('./Data/Superhost/Faces/' + uid + '.json'):
            print('-----face exists')
            continue
        if os.path.exists('./Data/Superhost/Photos/' + uid + '.jpg'):
            try:
                result = get_face_info('./Data/Superhost/Photos/' + uid + '.jpg')
                print(result)
                with open('./Data/Superhost/Faces/' + uid + '.json', 'w') as out:
                    out.write(json.dumps(result, indent=4))
            except:
                print('-----failed')
        else:
            print('-----photo dose not exist')


if __name__ == '__main__':
    if not os.path.exists('./Data/Superhost/Photos'):
        os.mkdir('./Data/Superhost/Photos')
    if not os.path.exists('./Data/Superhost/Faces'):
        os.mkdir('./Data/Superhost/Faces')
    face_analyse()
    with open('face_failed_list.txt', 'w') as out:
        out.write("\n".join(failed_list))
