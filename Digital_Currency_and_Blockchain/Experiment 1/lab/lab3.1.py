import hashlib
import random

p = 15161
g = 3
x = 101



def Prove():
    R = pow(g, r)
    # print(R)
    h = random.randint(1, p)  # hash函数太长了算不完，用randint替代一下
    # h=int(hashlib.md5(h).hexdigest(),16)
    # print(h)
    z = x * h + r
    return R, h, z


f = pow(g, x)
# print(f)


def Verif(z, h):
    if (pow(g, z) - pow(f, h) * R) % p != 0:
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
