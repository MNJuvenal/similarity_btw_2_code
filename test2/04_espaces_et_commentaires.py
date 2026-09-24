# Fonction pour calculer la somme
def somme_pairs(nombres):
    
    total = 0 # Initialisation
    
    for n in nombres:
        # On vérifie la parité
        if n % 2 == 0:
            total += n
            
    return total