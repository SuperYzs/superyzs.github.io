from ecc.curve import P256
import random


r = random.randint(1, P256.n)


def Setup():
    k = random.randint(1, P256.n)
    g = P256.G
    h = g * k
    return g, h


def Hash(G, H, M):
    h_0 = G * M + H * r
    return h_0


m = 516313135471534354415438154683156483514715246813546839164381543154687315413536418136456941835
g, h = Setup()
h_0 = Hash(g, h, m)

print("r = ", r)
print("g = ", g)
print("h = ", h_0)
print("Hash(K, M) = ", h_0.x)
