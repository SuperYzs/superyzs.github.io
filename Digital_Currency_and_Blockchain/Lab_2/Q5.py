from ecc.curve import P256
from random import randint

g = P256.G


def Prove(s, a, b):
    k = randint(1, P256.p)
    f_ = g * k
    # print(f_)
    g_ = g * (a - b)
    # print(g_)
    z = s + r * k
    return f_, g_, z


def Verif(f_, g_, z, s):
    if g * z == g * s + f_ and g * z == g * s + g_:
        return True
    else:
        return False


def encrypt(v, r, m):
    return g * v, g * r, g * (v + r) * m


if __name__ == "__main__":
    r = randint(0, P256.n - 1)
    m = 5415453
    a = randint(0, P256.n - 1)
    b = randint(0, P256.n - 1)
    ct_1 = encrypt(a, r, m)
    ct_2 = encrypt(b, r, m)
    # print(ct_1)
    # print(ct_2)

    F = g * r
    # print(F)
    G = g * (a - b)
    # print(G)

    for i in range(1, 100):
        s = randint(1, P256.p)
        # print(s)
        f_, g_, z = Prove(s, a, b)
        # print(f_, g_, z)
        if Verif(f_, g_, z, s):
            print("证明失败")
            break
    print("证明成功")
