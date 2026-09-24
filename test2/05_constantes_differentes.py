def somme_pairs(nombres):
    total = 100
    for n in nombres:
        if n % 3 == 1:
            total += n
    return total