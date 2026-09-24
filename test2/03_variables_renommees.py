def calculer_somme_nombres_pairs(liste_valeurs):
    resultat_final = 0
    for valeur in liste_valeurs:
        if valeur % 2 == 0:
            resultat_final += valeur
    return resultat_final