# -*- coding: utf-8 -*-

import json
import os
import pandas
import matplotlib.pyplot as plt
import numpy as np


def read_profile():
    file_in = open('./Data/Superhost/Profile_Super.txt')
    superhost_list_tmp = file_in.read().split('\n')
    superhost_list = []
    for superhost in superhost_list_tmp:
        if superhost != '':
            superhost_list.append(superhost.split('\t'))
    return superhost_list


def draw_face_charts():
    superhost_list = read_profile()
    gender = list()
    age = list()
    race = list()
    smiling = list()
    num = 0
    count = 0
    for superhost in superhost_list:
        uid = superhost[0]
        if os.path.exists('./Data/Superhost/Faces/' + uid + '.json'):
            with open('./Data/Superhost/Faces/' + uid + '.json', 'r') as file_in:
                face_data = json.load(file_in)
            num += 1
            if face_data['face']:
                count += 1
            for face in face_data['face']:
                gender.append(face['attribute']['gender']['value'])
                age.append(face['attribute']['age']['value'])
                race.append(face['attribute']['race']['value'])
                smiling.append(face['attribute']['smiling']['value'])
    print(float(count)/num)
    face_info = pandas.DataFrame(map(list, zip(*[gender, age, race, smiling])), columns=['gender', 'age', 'race', 'smiling'])
    gb_gender = face_info.groupby(['gender'])
    gb_race = face_info.groupby(['race'])
    gb_gender[['age']].count().rename(columns={'age': 'count'}).plot.pie(y='count', figsize=(5, 5), autopct='%.2f')
    plt.title('Gender of Airbnb superhosts')
    plt.savefig('./Result/gender.eps')
    plt.close()
    gb_race[['gender']].count().rename(columns={'gender': 'count'}).plot.pie(y='count', figsize=(5, 5), autopct='%.2f')
    plt.title('Race of Airbnb superhosts')
    plt.savefig('./Result/race.eps')
    plt.close()
    plt.plot(np.sort(age), np.linspace(0, 1, len(age)))
    plt.title('CDF of Airbnb superhosts age')
    plt.xlabel('Age')
    plt.ylabel('CDF')
    plt.savefig('./Result/CDF_age.eps')
    plt.close()
    plt.plot(np.sort(smiling), np.linspace(0, 1, len(smiling)))
    plt.title('CDF of Airbnb superhosts smiling index')
    plt.xlabel('Smiling index')
    plt.ylabel('CDF')
    plt.savefig('./Result/CDF_smiling.eps')
    plt.close()


if __name__ == '__main__':
    draw_face_charts()
