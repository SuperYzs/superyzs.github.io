import Q2
import sympy
from random import randint


def encode_DDT(x_, y):
    y, y_ = Q2.Eval(Q2.M, x_, y)
    return y, y_


def decode_DDT(y, y_):
    td = Q2.TrapGen(Q2.M)
    x1, x = Q2.Invert(td, y, y_, c)
    return x1, x


if __name__ == "__main__":
    x_ = sympy.Matrix([randint(0, pow(2, 15) - 1) for _ in range(int(Q2.n))])
    y = [Q2.g for _ in range(int(Q2.n))]
    c = [Q2.g - Q2.g for _ in range(int(Q2.n))]
    g_ = [Q2.g for _ in range(int(Q2.n))]

    for i in range(0, Q2.n):
        g_[i] = Q2.g * x_[i]
    print("明文为：", x_)
    print("陷门为：", Q2.M)
    print("g^x_： ", g_)

    y, y_ = encode_DDT(x_, y)
    print("签名：", y)

    x1, x = decode_DDT(y, y_)
    print("验证：", x)

    print("验证结果：", x == g_)
