def somme_pairs(nombres):
    return sum(filter(lambda x: x % 2 == 0, nombres))