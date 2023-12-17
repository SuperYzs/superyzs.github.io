import random

p = 15161
f = 3
g = 5
r = 101


def Prove(s):
    k_1 = random.randint(1, p)
    # print(k_1)
    k_2 = random.randint(1, p)
    # print(k_2)
    f_ = pow(f, k_1)
    # print(f_)
    g_ = pow(g, k_2)
    z_1 = s + r * k_1
    z_2 = s + r * k_2
    return f_, g_, z_1, z_2


F = pow(f, r)
# print(F)
G = pow(g, r)
# print(G)


def Verif(f_, g_, z_1, z_2, s):
    if (pow(f, z_1) - pow(f, s) * f_) % p == 0 and (
        pow(g, z_2) - pow(g, s) * g_
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
