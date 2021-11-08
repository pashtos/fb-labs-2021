def gcd_ext(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_ext(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def obernenyi(elem, mod):
    gcd_ = gcd_ext(elem, mod)
    if gcd_[0] == 1:
        return gcd_[1] % mod
    else:
        return -1


def module_equation(a: int, b: int, n):
    d = gcd_ext(a, n)[0]
    if d != -1:
        if d == 1:
            return (obernenyi(a, n) * b) % n
        elif b % d:
            return -1
        else:
            answers = []
            x = module_equation(a // d, b // d, n // d)
            answers.append(x)
            for i in range(1, d):
                answers.append(x + (n // d) * i)
            return answers
    return -1

