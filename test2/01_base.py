def somme_pairs(nombres):
    total = 0
    for n in nombres:
        if n % 2 == 0:
            total += n
    return total