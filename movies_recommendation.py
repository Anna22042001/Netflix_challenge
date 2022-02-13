import numpy
import math
import time
import sys
link = sys.argv[1]
f = open(link, "r")
lines = f.readlines()
users = dict()
movies = dict()
users_1 = dict()
movies_1 = dict()
for line in lines:
    line = line[:-1]
    line = line.split(",")
    try:
        movies_rated = users[line[0]]
        movies_rated[line[1]] = float(line[2])
        movies_rated_1 = users_1[line[0]]
        movies_rated_1[line[1]] = float(line[2])
    except:
        users[line[0]] = dict()
        users[line[0]][line[1]] = float(line[2])
        users_1[line[0]] = dict()
        users_1[line[0]][line[1]] = float(line[2])
    try:
        user_rate = movies[line[1]]
        user_rate[line[0]] = float(line[2])
        user_rate_1 = movies_1[line[1]]
        user_rate_1[line[0]] = float(line[2])
    except:
        movies[line[1]] = dict()
        movies[line[1]][line[0]] = float(line[2])
        movies_1[line[1]] = dict()
        movies_1[line[1]][line[0]] = float(line[2])


def normalize():
    for u_key in users.keys():
        mean = sum(users[u_key].values()) / len(users[u_key].values())
        for k in users[u_key].keys():
            users[u_key][k] -= mean
            movies[k][u_key] -= mean


normalize()

def cosine_user(u1, u2):
    movies_lst1 = users[u1]
    movies_lst2 = users[u2]
    up = 0
    for k in movies_lst1.keys():
        try:
            up += float(movies_lst1[k]) * float(movies_lst2[k])
        except:
            continue
    summ1 = 0
    for v in movies_lst1.values():
        summ1 += float(v) ** 2
    summ2 = 0
    for v in movies_lst2.values():
        summ2 += float(v) ** 2
    down = math.sqrt(summ1) * math.sqrt(summ2)
    return up / down


def cosine_movie(u1, u2):
    user_lst1 = movies[u1]
    user_lst2 = movies[u2]
    up = 0
    for k in user_lst1.keys():
        try:
            up += float(user_lst1[k]) * float(user_lst2[k])
        except:
            continue
    summ1 = 0
    for v in user_lst1.values():
        summ1 += float(v) ** 2
    summ2 = 0
    for v in user_lst2.values():
        summ2 += float(v) ** 2
    down = math.sqrt(summ1) * math.sqrt(summ2)
    return up / down


save_key = list()
result = dict()
for m_k in movies.keys():
    if int(m_k) <= 1000:
        save_key.append(m_k)
        result[m_k] = [0, 0]

users_rate = list()
for k in users.keys():
    if k == "600": continue
    similar = cosine_user("600", k)
    users_rate.append((k, similar))
users_rate.sort(key=lambda x: x[1], reverse=True)
similar_users = [users_rate[i][0] for i in range(10)]
for k in save_key:
    summ = 0
    countt = 0
    for u in similar_users:
        try:
            summ += users_1[u][k]
            countt += 1
        except:
            continue
    if countt == 0:
        continue
    result[k][0] = summ / countt
similar_movies = dict()
for k in save_key:
    similar_movies[k] = list()
    for ki in movies.keys():
        if ki == k: continue
        try:
            similar_movies[k].append((ki, cosine_movie(k, ki)))
        except:
            continue
    similar_movies[k].sort(key=lambda x: x[1], reverse=True)
    similar_movies[k] = similar_movies[k][:10]


for k in save_key:
    summ = 0
    countt = 0
    for tup in similar_movies[k]:
        ki = tup[0]
        try:
            summ += users_1["600"][ki]
            countt += 1
        except:
            continue
    if countt == 0:
        continue
    result[k][1] = summ / countt
user_based = sorted(result.items(), key=lambda x: (-x[1][0], int(x[0])))
item_based = sorted(result.items(), key=lambda x: (-x[1][1], int(x[0])))
user_based = user_based[:20]
item_based = item_based[:40]
result = ""
for i in range(5):
    print(str(user_based[i][0]) + "\t" + str(user_based[i][1][0]))
for i in range(5):
    print(str(item_based[i][0])+"\t"+str(item_based[i][1][1]))
