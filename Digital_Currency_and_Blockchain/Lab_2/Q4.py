from ecc.key import gen_keypair
from ecc.curve import P256, Point
from ecc.cipher import ElGamal


def KGen():
    sk, pk = gen_keypair(P256)
    return pk, sk


def Enc(pk, m):
    cipher_elg = ElGamal(P256)
    c1, c2 = cipher_elg.encrypt(m, pk)
    # print(c1,c2)
    return c1, c2


def Dec(sk, ct):
    cipher_elg = ElGamal(P256)
    m = cipher_elg.decrypt(sk, ct[0], ct[1])
    return m


if __name__ == "__main__":
    pk, sk = KGen()
    # print(pk,sk)

    m = "hello world!".encode("utf-8")
    print("明文为", m)
    ct = Enc(pk, m)
    print("公钥和私钥分别为：", ct)
    m = Dec(sk, ct)
    print("解密获得的明文为：", m)
