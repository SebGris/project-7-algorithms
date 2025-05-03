import csv
from itertools import combinations
import time  # Importation du module time pour mesurer le temps d'exécution


# Définir une classe pour représenter une action
class Action:
    def __init__(self, nom, cout, benefPourcent):
        self.nom = nom
        self.cout = cout
        self.benefPourcent = benefPourcent
        self.profit_estime = round(cout * (benefPourcent / 100), 2)


# Fonction pour calculer le profit total d'un portefeuille
def calculer_profit(portefeuille):
    return sum(action.profit_estime for action in portefeuille)


# Fonction pour vérifier si un portefeuille est valide (respecte le budget)
def est_valide(portefeuille, budget_max):
    return sum(action.cout for action in portefeuille) <= budget_max


# Fonction pour générer toutes les combinaisons possibles d'actions
def generer_combinations(liste_actions):
    toutes_combinations = []
    n = len(liste_actions)
    # Générer toutes les combinaisons possibles de 0 à n actions
    for r in range(n + 1):
        toutes_combinations.extend(combinations(liste_actions, r))
    return toutes_combinations


# Fonction pour trouver le meilleur portefeuille
def trouver_meilleur_portefeuille(liste_actions, budget_max):
    meilleur_portefeuille = []
    meilleur_profit = 0

    # Générer toutes les combinaisons possibles d'actions
    toutes_combinations = generer_combinations(liste_actions)

    # Évaluer chaque combinaison
    for combinaison in toutes_combinations:
        if est_valide(combinaison, budget_max):
            profit = calculer_profit(combinaison)
            if profit > meilleur_profit:
                meilleur_profit = profit
                meilleur_portefeuille = combinaison

    return meilleur_portefeuille


# Fonction pour charger les actions à partir d'un fichier CSV
def load_actions_from_csv(file_path):
    actions = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Création d'une instance de la classe Action pour chaque ligne
            # supprime le % de la colonne Bénéfice (%)
            # et convertit en entier
            action = Action(
                nom=row['Actions #'],
                cout=int(row['Coût par action (en euros)']),
                benefPourcent=int(
                    row['Bénéfice (après 2 ans)'].replace('%', '')
                )
            )
            # Ajout de l'action à la liste
            actions.append(action)
    return actions


# Exemple d'utilisation
def main():
    # Chemin vers le fichier CSV
    csv_file = "Liste+d'actions+-+P7+Python+-+Feuille+1.csv"
    # Liste des actions disponibles
    liste_actions = load_actions_from_csv(csv_file)

    budget_max = 500  # Budget maximal par client

    start_time = time.time()
    # Trouver le meilleur portefeuille
    meilleur_portefeuille = trouver_meilleur_portefeuille(liste_actions, budget_max)
    combinations_generation_time = time.time() - start_time
    print(f"Temps d'exécution : {combinations_generation_time:.2f} secondes")

    # Afficher le résultat
    print("Le portefeuille qui maximise le profit est :")
    for action in meilleur_portefeuille:
        print(f"{action.nom} (Coût: {action.cout}, Profit estimé: {action.profit_estime})")


if __name__ == "__main__":
    main()
