import random


def TrapGen(p, q):  # 生成计算密钥与陷门
    K = p
    td = pow(K, -1, (p - 1) * (q - 1))
    return K, td


def Eval(K, x):  # 利用计算密钥和信息生成单向函数输出
    y = pow(x, K, n)
    return y


def Invert(td, y):  # 根据单向函数输出以及陷门，计算信息
    x = pow(y, td, n)
    return x


def is_prime(n):
    if n <= 1 or (n % 2 == 0 and n > 2):
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def generate_large_prime(start, end):
    while True:
        p = random.randrange(start, end)
        if is_prime(p):
            return p


# 生成两个大素数
p = generate_large_prime(10**5, 10**6)
q = generate_large_prime(10**5, 10**6)

n = p * q
m = 4314141445
print("明文为：", m)
K, td = TrapGen(p, q)
print("密钥为：", K, "陷门为：", td)
Y = Eval(K, m)
print("输出密文为：", Y)
X = Invert(td, Y)
print("解密得到的明文为：", X)
