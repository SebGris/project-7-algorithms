import csv
import time
import os

CSV_FOLDER = "csv_files"


class Action:
    """
    Classe représentant une action avec son nom, son coût et son bénéfice.
    """
    def __init__(self, name, cost, benefice_pourcent=None, profit_euros=None):
        self.name = name
        self.cost = cost

        if benefice_pourcent is not None:
            self.benefice_pourcent = benefice_pourcent
            self.profit_euros = round(cost * (benefice_pourcent / 100), 2)
        elif profit_euros is not None:
            self.profit_euros = profit_euros
            self.benefice_pourcent = round((profit_euros / cost) * 100, 2)
        else:
            raise ValueError("Vous devez fournir soit 'benefice_pourcent', soit 'profit_euros'.")


def get_column_mapping(file_name):
    """
    Map the column names from the CSV file to the Action class attributes.
    """
    column_mapping = {
        "Liste+d'actions+-+P7+Python+-+Feuille+1.csv": {
            "name": "Actions #",
            "cost": "Coût par action (en euros)",
            "benefice_or_profit": "Bénéfice (après 2 ans)"
        },
        "dataset1_Python+P7.csv": {
            "name": "name",
            "cost": "price",
            "benefice_or_profit": "profit"
        },
        "dataset2_Python+P7.csv": {
            "name": "name",
            "cost": "price",
            "benefice_or_profit": "profit"
        }
    }
    mapping = column_mapping.get(file_name)
    if not mapping:
        raise ValueError(f"Le fichier {file_name} n'est pas pris en charge.")
    return mapping


def map_row_to_action(row, mapping):
    """
    Map a row from the CSV file to an Action object based on the provided mapping.
    """
    name = row[mapping["name"]]
    cost_value = float(row[mapping["cost"]])
    cost = round(cost_value, 2) if cost_value % 1 != 0 else int(cost_value)
    benefice_str = row[mapping["benefice_or_profit"]]
    if '%' in benefice_str:
        benefice_pourcent = int(benefice_str.replace('%', ''))
        profit_euros = None
    else:
        benefice_pourcent = None
        profit_euros = float(benefice_str)
    return Action(name=name, cost=cost, benefice_pourcent=benefice_pourcent, profit_euros=profit_euros)


def load_actions_from_csv(file_path):
    """
    Load actions from a CSV file and return a list of Action objects.
    """
    file_name = os.path.basename(file_path)
    mapping = get_column_mapping(file_name)
    with open(file_path, mode='r', encoding='utf-8') as file:
        return [map_row_to_action(row, mapping) for row in csv.DictReader(file)]


def knapsack_optimization(action_list, budget_max):
    """
    Optimise le choix des actions à acheter en fonction du budget maximum.
    Utilise l'algorithme du sac à dos (Knapsack Problem) pour maximiser le bénéfice.
    """
    if budget_max % 1 != 0:
        # If the budget is a float, multiply it by 100 to work with integers.
        budget_max = int(budget_max * 100)
        # costs and profits multiplied by 100
        action_list = [
            Action(
                action.name,
                action.cost * 100,
                profit_euros=action.profit_euros * 100
            )
            for action in action_list
        ]

    # Total number of shares
    n = len(action_list)

    # Initialising a table for dynamic programming
    # dp[i][w] represents the maximum profit achievable with the first i actions and a budget w
    dp = [[0 for _ in range(budget_max + 1)] for _ in range(n + 1)]  # from 0 to 20

    # Iterate over each action O(n * budget_max)
    for i in range(1, n + 1):  # from 1 to 20
        action = action_list[i - 1]
        cost = action.cost
        profit = action.profit_euros
        # Iterate over each possible budget
        for budget in range(budget_max + 1):  # range start to 0
            if cost <= budget:
                # Maximum profit including the current action
                previous_action_profit_for_budget = dp[i - 1][budget]
                best_profit_action = dp[i - 1][budget - cost]
                dp[i][budget] = max(previous_action_profit_for_budget, best_profit_action + profit)
            else:
                # Maximum profit excluding the current action
                dp[i][budget] = dp[i - 1][budget]

    # Trace back to find the selected actions
    selected_actions = []
    budget = budget_max
    for i in range(n, 0, -1):  # from 20 to 0 (0 is not included)
        if dp[i][budget] != dp[i - 1][budget]:
            action = action_list[i - 1]
            selected_actions.append(action.name)
            budget -= action.cost

    total_cost = sum(action.cost for action in action_list if action.name in selected_actions)
    total_profit = dp[n][budget_max]

    return selected_actions, total_cost, total_profit


def main():
    """
    Fonction principale pour exécuter le programme. 
    Charge les actions depuis les fichiers CSV, effectue l'optimisation du sac à dos
    et affiche les résultats.
    """
    csv_files_names = ["Liste+d'actions+-+P7+Python+-+Feuille+1.csv", "dataset1_Python+P7.csv", "dataset2_Python+P7.csv"]
    max_budget = 500
    start_time = time.time()
    # Utilisation de l'optimisation par programmation dynamique
    for csv_file in csv_files_names:
        # Chemin complet du fichier CSV
        csv_file = os.path.join(CSV_FOLDER, csv_file)
        print(f"Traitement du fichier : {csv_file}")
        # Chargement des actions depuis le fichier CSV
        action_list = load_actions_from_csv(csv_file)
        # Optimisation du sac à dos
        selected_actions, total_cost, total_profit = knapsack_optimization(action_list, max_budget)
        # Affichage des résultats
        print(f"Actions sélectionnées : {', '.join(selected_actions)}")
        print(f"Coût total : {total_cost} €")
        print(f"Bénéfice total : {total_profit:.2f} €\n")

    execution_time = time.time() - start_time
    print(f"Temps d'exécution : {execution_time:.2f} secondes")


if __name__ == "__main__":
    main()
