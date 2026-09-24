def est_pair(n):
    return n % 2 == 0

def somme_pairs(nombres):
    total = 0
    for n in nombres:
        if est_pair(n):
            total += n
    return total