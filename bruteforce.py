import csv
import time
from math import comb
from tqdm import tqdm


class Action:
    def __init__(self, nom, cout, benefPourcent):
        self.nom = nom
        self.cout = cout
        self.benefice_euros = round(cout * (benefPourcent / 100), 2)


def load_actions_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        return [
            Action(
                nom=row['Actions #'],
                cout=int(row['Coût par action (en euros)']),
                benefPourcent=int(row['Bénéfice (après 2 ans)'].replace('%', ''))
            )
            for row in csv.DictReader(file)
        ]


def calculate_profit_and_cost(combinaison):
    total_cost = sum(action.cout for action in combinaison)
    total_profit = sum(action.benefice_euros for action in combinaison)
    return total_cost, total_profit


def generate_combinations(action_list, budget_max):
    combinaisons = []
    n = len(action_list)
    total_combinations = sum(comb(n, i) for i in range(1, n + 1))
    with tqdm(total=total_combinations, desc="Génération des combinaisons") as progress_bar:
        for i in range(1, n + 1):
            for combinaison in combinations(action_list, i):
                total_cost, total_profit = calculate_profit_and_cost(combinaison)
                if total_cost <= budget_max:
                    combinaisons.append(([action.nom for action in combinaison], total_cost, total_profit))
                progress_bar.update(1)
    return combinaisons

def combinations(iterable, r):
    """
    Génère toutes les combinaisons possibles de longueur r à partir des éléments de l'itérable.
    
    Arguments :
        iterable : Une séquence ou un itérable (par exemple, une liste, une chaîne de caractères).
        r : La longueur des combinaisons souhaitées.
    
    Retourne :
        Une liste de tuples, où chaque tuple représente une combinaison unique de longueur r.
    
    Exemple :
        combinations('ABCD', 2) --> [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'D')]
    """
    n = len(iterable)  # Nombre total d'éléments dans l'itérable.
    if r > n:  # Si r est plus grand que n, il n'y a pas de combinaisons possibles.
        return []
    indices = list(range(r))  # Indices initiaux pour la première combinaison.
    # Première combinaison : les r premiers éléments de l'itérable.
    result = [tuple(iterable[i] for i in indices)]
    while True:
        # Trouver le premier indice (en partant de la fin) qui peut être incrémenté.
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            # Si aucun indice ne peut être incrémenté, toutes les combinaisons ont été générées.
            return result
        indices[i] += 1  # Incrémenter l'indice trouvé.
        # Réinitialiser les indices suivants pour maintenir l'ordre croissant.
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        # Ajouter la nouvelle combinaison générée à la liste des résultats.
        result.append(tuple(iterable[i] for i in indices))

def write_results_to_file(results, output_file):
    header = f"{'Actions':<145} {'Coût total (€)':<15} {'Bénéfice (€)':<15}\n"
    separator = "-" * 175 + "\n"
    with open(output_file, mode="w", encoding="utf-8") as file:
        file.write("Combinaisons d'actions respectant le budget (triées par bénéfice) :\n")
        file.write(header)
        file.write(separator)
        with tqdm(total=len(results), desc="Écriture dans le fichier") as progress_bar:
            for action_names, total_cost, profit in results:
                file.write(f"{' '.join(action_names):<145} {total_cost:<15} {profit:.2f}\n".replace('.', ','))
                progress_bar.update(1)


def main():
    csv_file = "Liste+d'actions+-+P7+Python+-+Feuille+1.csv"
    action_list = load_actions_from_csv(csv_file)
    start_time = time.time()
    max_budget = 500
    valid_combinations = generate_combinations(action_list, max_budget)
    results = sorted(valid_combinations, key=lambda x: x[2], reverse=True)
    write_results_to_file(results, "resultat_combinations.txt")
    print(f"Temps d'exécution total : {time.time() - start_time:.2f} secondes")

def test():
    test_a = combinations('ABCD', 2)
    print(test_a)


if __name__ == "__main__":
    #main()
    test()
