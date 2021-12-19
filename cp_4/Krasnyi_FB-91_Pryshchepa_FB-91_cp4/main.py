from random import *

candidates = []


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def single_test(n, a):
    exp = n - 1
    while not exp & 1:
        exp >>= 1
    if pow(a, exp, n) == 1:
        return True
    while exp < n - 1:
        if pow(a, exp, n) == n - 1:
            return True
        exp <<= 1
    return False


def miller_rabin(n, k=40):
    for i in range(k):
        a = randint(2, n - 1)
        if not single_test(n, a):
            return False
    return True


def generate_pairs():
    while True:
        p1 = randrange(10 ** 70, 10 ** 71 - 1)
        if miller_rabin(p1):
            break
        candidates.append(p1)
    while True:
        q1 = randrange(10 ** 70, 10 ** 71 - 1)
        if miller_rabin(q1):
            break
        candidates.append(q1)
    while True:
        p2 = randrange(10 ** 70, 10 ** 71 - 1)
        if miller_rabin(p2):
            break
        candidates.append(p2)
    while True:
        q2 = randrange(10 ** 70, 10 ** 71 - 1)
        if miller_rabin(q2):
            break
        candidates.append(q2)
    if p1 * q1 > p2 * q2:
        p1, p2 = p2, p1
        q1, q2 = q2, q1
    return [[p1, q1], [p2, q2]]


def generate_key_pair(p, q):
    n = p * q
    oiler = (p - 1) * (q - 1)
    e = randint(2, oiler - 1)
    while gcd(e, oiler) != 1:
        e = randint(2, oiler - 1)
    d = pow(e, -1, oiler)
    return [n, e, d]


def encrypt(m, n, e):
    return pow(m, e, n)


def decrypt(c, d, n):
    return pow(c, d, n)


def sign(m, d, n):
    return [m, pow(m, d, n)]


def verify(m, s, e, n):
    return m == pow(s, e, n)


def send_key(k, e1, n1, d, n):
    k1 = pow(k, e1, n1)
    s = pow(k, d, n)
    s1 = pow(s, e1, n1)
    return [k1, s1]


def receive_key(k1, s1, d1, n1):
    k = pow(k1, d1, n1)
    s = pow(s1, d1, n1)
    return [k, s]


candidates_ = open("key_candidates.txt", "w", encoding="utf-8")
pairs = generate_pairs()
res = ""
for i in candidates:
    res += str(i) + "\n"
candidates_.write(res)
candidates_.close()
print("p1, q1: ", *pairs[0])
print("p2, q2: ", *pairs[1])
rsa_keys_a = generate_key_pair(*pairs[0])
rsa_keys_b = generate_key_pair(*pairs[1])
print("n, e, d for abonent A")
print(*rsa_keys_a, sep="\n")
print("n1, e1, d1 for abonent B")
print(*rsa_keys_b, sep="\n")

print("\n\nFor abonent A:\n")
message = randint(0, rsa_keys_a[0])
print("Message: ", message)
cipher = encrypt(message, rsa_keys_a[0], rsa_keys_a[1])
print("Encrypted message: ", cipher)
decrypted_message = decrypt(cipher, rsa_keys_a[2], rsa_keys_a[0])
print("Decrypted message: ", decrypted_message)
if message == decrypted_message:
    print("Decryption is successful")
else:
    print("Decryption failed")

signed_message = sign(message, rsa_keys_a[2], rsa_keys_a[0])
if verify(signed_message[0], signed_message[1], rsa_keys_a[1], rsa_keys_a[0]):
    print("Verification state: OK")
else:
    print("Verification state: failure")

print("\n\nFor abonent B:\n")
message_ = randint(0, rsa_keys_b[0])
print("Message: ", message_)
cipher_ = encrypt(message_, rsa_keys_b[0], rsa_keys_b[1])
print("Encrypted message: ", cipher_)
decrypted_message_ = decrypt(cipher_, rsa_keys_b[2], rsa_keys_b[0])
print("Decrypted message: ", decrypted_message_)
if message_ == decrypted_message_:
    print("Decryption is successful")
else:
    print("Decryption failed")

signed_message_ = sign(message_, rsa_keys_b[2], rsa_keys_b[0])
if verify(signed_message_[0], signed_message_[1], rsa_keys_b[1], rsa_keys_b[0]):
    print("Verification state: OK")
else:
    print("Verification state: failure")
print("\n\n\n")
k = randint(0, rsa_keys_a[0])
print(f"A generated a secret value k: {k}")
a_send = send_key(k, rsa_keys_b[1], rsa_keys_b[0], rsa_keys_a[2], rsa_keys_a[0])
print(f"A created a message (k1, s1): ({a_send[0]}, {a_send[1]})")
b_receive = receive_key(a_send[0], a_send[1], rsa_keys_b[2], rsa_keys_b[0])
print(f"B received (k, s): ({b_receive[0]}, {b_receive[1]}")
# pairs = generate_pairs()
# rsa_keys_a = generate_key_pair(*pairs[0])
# n1 = rsa_keys_a[0]
# e1 = rsa_keys_a[1]
# d1 = rsa_keys_a[2]
# n1_hex = hex(n1)
# e1_hex = hex(e1)
# d1_hex = hex(d1)
#
# hex_ = "DA6E298E5B6D042905DDE576A46E94DED32B189D358E2AAD8E663FA86049A61720774508556714AF79BB7001B9B9B47042AD062C7EC499488F895F6414190BCD"
# n2 = (int(float.fromhex(hex_)))
# e2 = int(float.fromhex("10001"))
# message = randint(0, 128)
# a_send = send_key(message, e2, n2, d1, n1)
# k1 = a_send[0]
# s1 = a_send[1]
# k1_hex = hex(k1)
# s1_hex = hex(s1)
# print(k1_hex[2:], s1_hex[2:], sep="\n")
# print(n1_hex[2:])
# print(e1_hex[2:])