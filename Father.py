
def F(n):
    if n == 0:
        return 0
    while n % 10 == 0:
        n //= 10
    return n % 10

def S(p, q):
    total = 0

    if p > q:
        return total

    if q - p < 100:
        for i in range(p, q + 1):
            total += F(i)
        return total

    while p % 10 != 0 and p <= q:
        total += F(p)
        p += 1

    while (q + 1) % 10 != 0 and q >= p:
        total += F(q)
        q -= 1

    if p > q:
        return total

    blocks = (q - p + 1) // 10
    total += blocks * 45

    return total

while True:
    line = input().strip()
    if not line:
        continue
    p, q = map(int, line.split())
    if p < 0 and q < 0:
        break
    if p > q:
        p, q = q, p
    print(S(p, q))
