from ecc.curve import P256
import random

r_1 = random.randint(1, P256.n)
r_2 = random.randint(1, P256.n)


def SetupInsecure():
    k = random.randint(1, P256.n)
    g = P256.G
    h = g * k
    return g, h, k


def FindCol(G, H, K):
    X_1 = 4165135134151353133141468746886478468764874686487468469831483619865466849646815468175647815
    X_2 = r_1 * K + X_1 - r_2 * K
    return X_1, X_2


def Hash(G, H, M, r):
    h = G * M + H * r
    return h


g, h, k = SetupInsecure()
x_1, x_2 = FindCol(g, h, k)
h_1 = Hash(g, h, x_1, r_1)
h_2 = Hash(g, h, x_2, r_2)
print("x_1 = ", x_1)
print("x_2 = ", x_2)
print("r_1 = ", r_1)
print("r_2 = ", r_2)
print("g = ", g)
print("h = ", h)
print("k = ", k)
print("Hash(K, M) = ", h_1.x)
print("Hash(H, M) = ", h_2.x)


if h_1 == h_2:
    print("True")
else:
    print("False")
