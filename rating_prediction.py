import numpy
import numpy as np
import math
import os
import sys
f = open(sys.argv[1], "r")
f_test = open(sys.argv[2], "r")
test = f_test.readlines()
lines = f.readlines()
users = dict()
movies = dict()
users_count = dict()
movies_count = dict()
sum_non_blank = 0
for line in lines:
    line = line[:-1]
    line = line.split(",")
    sum_non_blank += float(line[2])
    users_count[line[0]] = 1
    movies_count[line[1]] = 1
    try:
        movies_rated = users[line[0]]
        movies_rated[line[1]] = float(line[2])
    except:
        users[line[0]] = dict()
        users[line[0]][line[1]] = float(line[2])
    try:
        user_rate = movies[line[1]]
        user_rate[line[0]] = float(line[2])
    except:
        movies[line[1]] = dict()
        movies[line[1]][line[0]] = float(line[2])
avg_non_blank = sum_non_blank / len(lines)
lst_users = [0] * len(users_count.keys())
i = 0
for k in users_count.keys():
    users_count[k] = i
    lst_users[i] = k
    i += 1
lst_movies = [0] * len(movies_count.keys())
i = 0
for k in movies_count.keys():
    movies_count[k] = i
    lst_movies[i] = k
    i += 1
normal_save = [[0 for i in range(len(lst_movies))] for j in range(len(lst_users))]
normal_user = [0 for i in range(len(lst_users))]
normal_movie = [0 for i in range(len(lst_movies))]
M = [[None for i in range(len(lst_movies))] for j in range(len(lst_users))]


def normalize():
    for u_key in users.keys():
        mean = sum(users[u_key].values()) / len(users[u_key].values())
        for k in users[u_key].keys():
            users[u_key][k] -= mean
            movies[k][u_key] -= mean
        normal_user[users_count[u_key]] += mean
    for m_key in movies.keys():
        mean = sum(movies[m_key].values()) / len(movies[m_key].values())
        for k in movies[m_key].keys():
            movies[m_key][k] -= mean
            users[k][m_key] -= mean
        normal_movie[movies_count[m_key]] += mean


normalize()
for u_key in users.keys():
    for m_key in users[u_key].keys():
        M[users_count[u_key]][movies_count[m_key]] = float(users[u_key][m_key])

K = 3
M = numpy.array(M)
each = math.sqrt(avg_non_blank / 3)
U = np.full((len(M), K), each)
V = np.full((len(M[0]), K), each)


def UV_composition(M, U, V, K, steps=340, alpha=0.0003, beta=0.01):
    V_T = V.T
    for step in range(steps):
        for i in range(len(M)):
            for j in range(len(M[i])):
                if M[i][j]:
                    eij = M[i][j] - numpy.dot(U[i, :], V_T[:, j])
                    for k in range(K):
                        U[i][k] = U[i][k] + alpha * (2 * eij * V_T[k][j] - beta * U[i][k])
                        V_T[k][j] = V_T[k][j] + alpha * (2 * eij * U[i][k] - beta * V_T[k][j])
        Loss = 0
        for i in range(len(M)):
            for j in range(len(M[i])):
                if M[i][j]:
                    Loss = Loss + (M[i][j] - numpy.dot(U[i, :], V_T[:, j]))**2
                    for k in range(K):
                        Loss = Loss + (beta / 2) * (U[i][k]**2 + V_T[k][j]**2)
        print(Loss/len(lines))
        if Loss/len(lines) < 0.6:
            break
    return U, V_T.T


U_new, V_new = UV_composition(M, U, V, K)
M_new = numpy.dot(U_new, V_new.T)
for i in range(len(M_new)):
    for j in range(len(M_new[0])):
        M_new[i][j] += normal_user[i] + normal_movie[j]

find = os.path.exists("output.txt")
with open("output.txt", "a" if find else "w") as f:
    for line in test:
        line = line[:-1]
        line = line.split(",")
        try:
            i = users_count[line[0]]
            j = movies_count[line[1]]
            rating = M_new[i][j]
        except:
            continue
        result = str(line[0]) + "," + str(line[1]) + "," + str(rating) + "," + str(line[3]) + "\n"
        f.write(result)


"""

summ = 0
countt = 0
for line in test:
    line = line.split(",")
    try:
        i = users_count[line[0]]
        j = movies_count[line[1]]
        summ += (float(line[2]) - nR[i][j]) ** 2
        countt += 1
    except:
        continue
print(math.sqrt(summ / countt))
"""
