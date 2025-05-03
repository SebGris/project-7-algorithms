import csv
import time
from itertools import combinations
from math import comb  # Importation pour calculer les coefficients binomiaux
from tqdm import tqdm


class Action:
    def __init__(self, nom, cout, benefPourcent):
        self.nom = nom
        self.cout = cout
        self.benefPourcent = benefPourcent
        self.benefice_euros = round(cout * (benefPourcent / 100), 2)


def load_actions_from_csv(file_path):
    """
    Charge les actions à partir d'un fichier CSV.

    :param file_path: Chemin vers le fichier CSV
    :return: Liste d'objets Action
    """
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


# Fonction pour calculer le profit total d'un portefeuille
def calculate_profit(combinaison):
    return sum(action.benefice_euros for action in combinaison)


# Fonction pour calculer le cout total d'un portefeuille
def calculate_total_cost(combinaison):
    return sum(action.cout for action in combinaison)


def generate_combinations(liste_actions, budget_max):
    """
    Génère toutes les combinaisons possibles d'actions respectant le budget.

    :param actions: Liste d'objets Action
    :param investissement_max: Budget maximum (en euros)
    :return: Liste des combinaisons sous forme de tuples
             (noms_actions, cout_total, benefice)
    """
    combinaisons = []
    n = len(liste_actions)
    total_combinations = sum(comb(n, i) for i in range(1, n + 1))
    # Utilisation de tqdm pour afficher la progression
    with tqdm(
        total=total_combinations,
        desc="Génération des combinaisons"
    ) as progress_bar:
        for i in range(1, n + 1):
            for combinaison in combinations(liste_actions, i):
                cout_total = calculate_total_cost(combinaison)
                if cout_total <= budget_max:
                    noms_actions = [action.nom for action in combinaison]
                    benefice = calculate_profit(combinaison)
                    combinaisons.append((noms_actions, cout_total, benefice))
                progress_bar.update(1)
    return combinaisons


# Exemple d'utilisation
def main():
    # Chemin vers le fichier CSV
    csv_file = "Liste+d'actions+-+P7+Python+-+Feuille+1.csv"
    # Liste des actions
    action_list = load_actions_from_csv(csv_file)
    max_budget = 500  # Budget maximal par client
    # Mesure du temps d'exécution
    start_time = time.time()
    valid_combinations = generate_combinations(action_list, max_budget)
    combinations_generation_time = time.time() - start_time
    print(f"Temps d'exécution : {combinations_generation_time:.2f} secondes")
    # Trie les résultats par bénéfice décroissant
    results = sorted(valid_combinations, key=lambda x: x[2], reverse=True)
    # Affichage formaté sous forme de tableau
    output_file = "resultat_combinations.txt"
    with open(output_file, mode="w", encoding="utf-8") as file:
        header = (
            f"{'Actions':<145} "
            f"{'Coût total (€)':<15} "
            f"{'Bénéfice (€)':<15}\n"
        )
        separator = "-" * 175 + "\n"
        file.write(
            "Combinaisons d'actions respectant le budget "
            "(triées par bénéfice) :\n"
        )
        file.write(header)
        file.write(separator)
        # Ajout de la jauge de progression pour l'écriture
        with tqdm(
            total=len(results),
            desc="Écriture dans le fichier"
        ) as progress_bar:
            for noms_actions, cout_total, benefice in results:
                actions_str = " ".join(noms_actions)
                formatted_line = (
                    f"{actions_str:<145} {cout_total:<15} {benefice:.2f}"
                ).replace('.', ',')
                file.write(formatted_line + "\n")
                progress_bar.update(1)

    execution_time = time.time() - start_time - combinations_generation_time
    print(f"Temps d'exécution : {execution_time:.2f} secondes")
    # Calcul et affichage du temps d'exécution
    execution_time = time.time() - start_time
    print(f"Résultat écrit dans le fichier : {output_file}")
    print(f"Temps d'exécution total : {execution_time:.2f} secondes")


if __name__ == "__main__":
    main()
