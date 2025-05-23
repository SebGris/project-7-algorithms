import csv
import time


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


def knapsack_optimization(action_list, budget_max):
    # Total number of shares
    n = len(action_list)

    # Initialising a table for dynamic programming
    # dp[i][w] represents the maximum profit achievable with the first i actions and a budget w
    dp = [[0 for _ in range(budget_max + 1)] for _ in range(n + 1)]  # from 0 to 20

    dp_update_log = [""] * (budget_max + 1)
    # Iterate over each action
    for i in range(1, n + 1):  # from 1 to 20
        action = action_list[i - 1]
        cost = action.cout
        profit = action.benefice_euros
        # Iterate over each possible budget
        for budget in range(budget_max + 1):  # range start to 0
            if cost <= budget:
                # Maximum profit including the current action
                dp[i][budget] = max(dp[i - 1][budget], dp[i - 1][budget - cost] + profit)
            else:
                # Maximum profit excluding the current action
                dp[i][budget] = dp[i - 1][budget]
            # Log pour suivre les mises à jour de dp
            if i == 7:
                dp_update_log[budget] = f"dp[{i}][{budget}] = {round(dp[i][budget], 2)}"

    # Log pour suivre les mises à jour de dp
    for str in dp_update_log:
        print(str)
    # Trace back to find the selected actions
    selected_actions = []
    budget = budget_max
    for i in range(n, 0, -1):  # from 20 to 0 (0 is not included)
        if dp[i][budget] != dp[i - 1][budget]:
            action = action_list[i - 1]
            selected_actions.append(action.nom)
            budget -= action.cout

    total_cost = sum(action.cout for action in action_list if action.nom in selected_actions)
    total_profit = dp[n][budget_max]

    return selected_actions, total_cost, total_profit


def write_results_to_file(results, output_file):
    header = f"{'Actions':<145} {'Coût total (€)':<15} {'Bénéfice (€)':<15}\n"
    separator = "-" * 175 + "\n"
    with open(output_file, mode="w", encoding="utf-8") as file:
        file.write("Combinaisons d'actions respectant le budget (triées par bénéfice) :\n")
        file.write(header)
        file.write(separator)
        for action_names, total_cost, profit in results:
            file.write(f"{' '.join(action_names):<145} {total_cost:<15} {profit:.2f}\n".replace('.', ','))


def main():
    csv_file = "Liste+d'actions+-+P7+Python+-+Feuille+1.csv"
    action_list = load_actions_from_csv(csv_file)
    start_time = time.time()
    max_budget = 500

    # Utilisation de l'optimisation par programmation dynamique
    selected_actions, total_cost, total_profit = knapsack_optimization(action_list, max_budget)
    combinations_generation_time = time.time() - start_time
    print(f"Temps d'exécution : {combinations_generation_time:.2f} secondes")
    # Écriture des résultats dans un fichier
    output_file = "resultat_knapsack.txt"
    results = [(selected_actions, total_cost, total_profit)]
    write_results_to_file(results, output_file)

    execution_time = time.time() - start_time - combinations_generation_time
    print(f"Temps d'exécution : {execution_time:.2f} secondes")
    # Calcul et affichage du temps d'exécution
    execution_time = time.time() - start_time
    print(f"Résultat écrit dans le fichier : {output_file}")
    print(f"Temps d'exécution total : {execution_time:.2f} secondes")

if __name__ == "__main__":
    main()
