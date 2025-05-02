from itertools import combinations

liste = [1, 2, 3, 4]


def generate_combinations(liste):
    combinaisons = []  # Liste pour stocker les combinaisons
    # boucle sur le nombre d'éléments dans chaque combinaison
    for i in range(1, len(liste) + 1):
        # utilise itertools.combinations pour générer les combinaisons
        combinaisons.extend(combinations(liste, i))
    return combinaisons  # Retourne la liste des combinaisons


# Appel de la fonction et affichage du résultat
resultat = generate_combinations(liste)
print(resultat)
