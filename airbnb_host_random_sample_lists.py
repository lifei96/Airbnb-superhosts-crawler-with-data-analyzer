# -*- coding: utf-8 -*-

import random
import os


def read_users_list():
    with open('./Data/Host/hostID.txt', 'r') as f:
        users_list = f.read().split('\n')
    return users_list


def random_sample_list(users_list, num, each):
    sample_list = random.sample(users_list, num * each)
    for i in range(0, num):
        with open('./Data/Host/host_sample_list_%d.txt' % i, 'w') as f:
            f.write('\n'.join(sample_list[i * each:(i + 1) * each]))


if __name__ == '__main__':
    if not os.path.exists('./Data/Host/'):
        os.mkdir('./Data/Host')
    random_sample_list(read_users_list(), 1, 100000)
