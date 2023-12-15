import hashlib
import random

p = 15161
g = 3
x = 101


def powermod(a, b):
    c = a
    for i in range(1, b):
        c = (c * a) % p
    return c


def Prove():
    R = powermod(g, r)
    # print(R)
    h = random.randint(1, p)  # hash函数太长了算不完，用randint替代一下
    # h=int(hashlib.md5(h).hexdigest(),16)
    # print(h)
    z = x * h + r
    return R, h, z


f = powermod(g, x)
# print(f)


def Verif(z, h):
    if (powermod(g, z) - powermod(f, h) * R) % p != 0:
        return True
    else:
        return False


for i in range(1, 100):
    r = random.randint(1, p)
    # print(r)
    R, h, z = Prove()
    if Verif(z, h):
        print("证明失败")
        break
print("证明成功")
