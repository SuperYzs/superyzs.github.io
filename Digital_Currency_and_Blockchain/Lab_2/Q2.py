import sympy
from random import randint
from ecc.curve import P256

k = 152
q = P256.n
g = P256.G
# n = int(math.log(q / 15)) + 1
n = 7


def createMatrix(rows, cols):
    arr = []
    for i in range(rows):
        col = [randint(0, pow(2, 15) - 1) for _ in range(cols)]
        arr.append(col)
    return sympy.Matrix(arr)


def BitInvert(y):
    for x in range(0, q):
        if g * x == y:
            return x
    return 0


def Eval(M, x_, y):
    y_ = M.multiply(x_) % q
    for i in range(0, n):
        y[i] = g * int(y_[i])
    # print(y,y_)
    return y, y_


def TrapGen(M):
    td = M.inv_mod(q)
    # print(M*td%q)
    return td


def Invert(td, y, y_, c):
    c_ = td.multiply(y_) % q
    for i in range(0, n):
        for j in range(0, n):
            c[i] = y[j] * td[i * n + j] + c[i]
        # c[i]=g* int(c_[i])
        # print(c[i],g* int(c_[i]))
    # print(c)
    return c_, c


# M = createMatrix(n, n)
M = sympy.Matrix(
    [
        [20263, 29624, 7140, 25192, 29950, 27715, 15590],
        [1868, 15776, 19457, 2504, 422, 29323, 21231],
        [21599, 6717, 7771, 31738, 3894, 3913, 15075],
        [772, 7756, 9507, 10095, 11506, 20200, 2480],
        [426, 22745, 21254, 19868, 24297, 28397, 204],
        [19932, 705, 14881, 26242, 14933, 17205, 22213],
        [28822, 12266, 9567, 10557, 22165, 41, 8349],
    ]
)
if __name__ == "__main__":
    x_ = sympy.Matrix([randint(0, pow(2, 15) - 1) for _ in range(int(n))])
    y = [g for _ in range(int(n))]
    c = [g - g for _ in range(int(n))]
    g_ = [g for _ in range(int(n))]

    Y = g * k
    X = BitInvert(Y)
    print("离散对数为：", X)
    y, y_ = Eval(M, x_, y)
    print("单项陷门函数的输出为：", y)
    td = TrapGen(M)
    for i in range(0, n):
        g_[i] = g * int(x_[i])
    # print(y)
    x1, x = Invert(td, y, y_, c)

    # print(x_ % q)
    # print(x1 % q)
    # print((x1 - x_) % q)

    print("g^x为：", g_)
    print("验证获得的数为：", x)
    print("验证结果", x == g_)
