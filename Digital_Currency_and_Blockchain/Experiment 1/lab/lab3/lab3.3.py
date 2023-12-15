import random

p = 15161
f = 3
g = 5
r = 101


def powermod(a, b):
    c = a
    for i in range(1, b):
        c = (c * a) % p
    return c


def Prove(s):
    k_1 = random.randint(1, p)
    # print(k_1)
    k_2 = random.randint(1, p)
    # print(k_2)
    f_ = powermod(f, k_1)
    # print(f_)
    g_ = powermod(g, k_2)
    z_1 = s + r * k_1
    z_2 = s + r * k_2
    return f_, g_, z_1, z_2


F = powermod(f, r)
# print(F)
G = powermod(g, r)
# print(G)


def Verif(f_, g_, z_1, z_2, s):
    if (powermod(f, z_1) - powermod(f, s) * f_) % p == 0 and (
        powermod(g, z_2) - powermod(g, s) * g_
    ) % p == 0:
        return True
    else:
        return False


for i in range(1, 100):
    s = random.randint(1, p)
    # print(s)
    f_, g_, z_1, z_2 = Prove(s)
    if Verif(f_, g_, z_1, z_2, s):
        print("证明失败")
        break
print("证明成功")
