import csv
import time
from itertools import combinations
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
    action_count = len(action_list)
    total_combinations = sum(comb(action_count, i) for i in range(1, action_count + 1))
    with tqdm(total=total_combinations, desc="Génération des combinaisons") as progress_bar:
        for i in range(1, action_count + 1):
            for combinaison in combinations(action_list, i):  # O(2^n)
                total_cost, total_profit = calculate_profit_and_cost(combinaison)
                if total_cost <= budget_max:
                    combinaisons.append(([action.nom for action in combinaison], total_cost, total_profit))
                progress_bar.update(1)
    return combinaisons


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


if __name__ == "__main__":
    main()
