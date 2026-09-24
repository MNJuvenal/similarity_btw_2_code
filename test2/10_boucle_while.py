def somme_pairs(nombres):
    total = 0
    i = 0
    while i < len(nombres):
        if nombres[i] % 2 == 0:
            total += nombres[i]
        i += 1
    return total