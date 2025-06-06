import csv
import os
import time
from itertools import combinations
from tqdm import tqdm

CSV_FOLDER = "csv_files"


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


def generate_combinations(action_list, budget_max):  # O(n * 2^n)
    combinaisons = []
    action_count = len(action_list)
    total_combinations = 2 ** action_count - 1  # O(2^n)
    with tqdm(total=total_combinations, desc="Génération des combinaisons") as progress_bar:
        for i in range(1, action_count + 1):  # O(n)
            for combinaison in combinations(action_list, i):  # O(2^n)
                total_cost, total_profit = calculate_profit_and_cost(combinaison)  # O(i)
                if total_cost <= budget_max:  # O(1)
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
    csv_file_path = os.path.join(CSV_FOLDER, csv_file)
    action_list = load_actions_from_csv(csv_file_path)
    start_time = time.time()
    max_budget = 500
    valid_combinations = generate_combinations(action_list, max_budget)
    combinations_generation_time = time.time() - start_time
    print(f"Temps d'exécution pour 'generate_combinations' : {combinations_generation_time:.2f} secondes")
    results = sorted(valid_combinations, key=lambda x: x[2], reverse=True)
    write_results_to_file(results, "resultat_combinations.txt")
    execution_time = time.time() - start_time - combinations_generation_time
    print(f"Temps d'exécution pour 'write_results_to_file' : {execution_time:.2f} secondes")
    print(f"Temps d'exécution total : {time.time() - start_time:.2f} secondes")


if __name__ == "__main__":
    main()
