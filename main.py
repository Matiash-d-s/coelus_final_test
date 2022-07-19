import numpy as np
import copy

#Добавить полимино
def add_pol(P, pol, t, a, b):
    P[a:a + t[0], b:b + t[1]] += pol
    return P

# Удалить полимино
def del_pol(P, pol, t, a, b):
    P[a:a + t[0], b:b + t[1]] -= pol
    return P

# Подсчет ошибки
def calc_mistake(P):
    inf = 1000
    s = np.sum(P[np.bitwise_and(P > 1, P < inf)])
    s += np.sum(P[P > inf])
    return s

# Создание полимино в виде матрицы
def polyomino(t):
    if t[2] == 0:
        sh = np.ones((t[0], t[1]))
    else:
        sh = np.zeros((t[0], t[1]))
        sh[:t[0], 0] = 1
        sh[0, 1:t[1]] += 1
    return sh

# Поворот полимино
def rotate(pol):
    pol = np.rot90(pol)
    return pol

# Укладка
def tiling(type_ship, cd, P):
    count = 0
    for t, c in zip(type_ship, cd):
        s = 1.0
        while s != 0.0:
            templ = polyomino(t)
            if c[2] > 0:
                for i in range(c[2]):
                    templ = rotate(templ)
                if c[2] != 2:
                    t[0], t[1] = t[1], t[0]
            P = add_pol(P, templ, t, c[0], c[1])
            count += 1
            s = calc_mistake(P)
            if s > 0:
                P = del_pol(P, templ, t, c[0], c[1])
                count -= 1
                if c[0] + 1 <= 3+POLE_SIZE - t[0]:
                    c[0] += 1
                elif c[1] + 1 <= 3+H_SIZE - t[1]:
                    c[1] += 1
                    c[0] = 3
                elif c[2] < 3:
                    c[2] += 1
                    c[0] = 3
                    c[1] = 3
                else:
                    return False, count - 1
    return True, count - 1

# Смена начальных координат
def recoord(cd, index):
    if cd[index][2] != 3:
        cd[index][2] += 1
        return cd
    else:
        cd[index][2] = 0
        index -= 1
        if index > -1:
            return recoord(cd, index)
        else:
            cd[index+1][2] = 4
            return cd
#Площадь всех полимино
def area(t):
    S = 0
    for i in t:
        if i[2]== 0:
            S+=i[0]*i[1]
        else:
            S+=i[0]+i[1]-1
    return S


print("Введите размер поля")
a,b=map(int,input().split())
POLE_SIZE = max(a,b)
H_SIZE = min(a,b)
# Сюда следует ввести параметры полимино, последний аргумент 0- опорный элемент 1 - L образный
type_ship = [[2,2,0],  [2, 3,1], [2, 2 ,1], [2, 2 ,1]]
inf = 1000
P0 = np.zeros((POLE_SIZE, H_SIZE))
count = 0
cd=[]
# Массив координат
for i in range(len(type_ship)):
    cd.append([3,3,0])
flag = False
s = area(type_ship)
if s > POLE_SIZE*H_SIZE:
    print(False)
    breakpoint()
while (flag == False) and (cd[0][2] != 4):
    P = np.ones((POLE_SIZE + 6, H_SIZE + 6)) * inf
    P[3:POLE_SIZE + 3, 3:H_SIZE + 3] = P0
    coordinats = copy.deepcopy(cd)
    flag, ind = tiling(type_ship, coordinats, P)
    cd = recoord(cd, ind)

print(flag)
