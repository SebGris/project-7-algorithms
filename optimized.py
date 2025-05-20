import csv
import time
import os
import pandas as pd

CSV_FOLDER = "csv_files"


class Action:
    """
    Class representing an action with its name, cost and benefit.
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


def load_actions_from(df):
    """
    Convertit un DataFrame pandas en liste d'objets Action pour les datasets.
    """
    mapping = {
        "name": "name",
        "cost": "price",
        "benefice_or_profit": "profit"
    }
    actions = []
    for _, row in df.iterrows():
        name = row[mapping["name"]]
        cost_value = float(row[mapping["cost"]])
        cost = round(cost_value, 2) if cost_value % 1 != 0 else int(cost_value)
        benefice_str = str(row[mapping["benefice_or_profit"]])
        if '%' in benefice_str:
            benefice_pourcent = int(benefice_str.replace('%', ''))
            profit_euros = None
        else:
            benefice_pourcent = None
            profit_euros = float(benefice_str)
        actions.append(Action(name=name, cost=cost, benefice_pourcent=benefice_pourcent, profit_euros=profit_euros))
    return actions


def display_dataframe_overview(df):
    """
    Displays the first 5 lines of the DataFrame.
    """
    print("Voici les 5 premières lignes du DataFrame :")
    print(df.head(5))
    print("\nVoici les 5 dernières lignes du DataFrame :")
    print(df.tail(5))
    print("\nVoici les informations sur le DataFrame :")
    print(df.info())
    print("\nVoici la description du DataFrame :")
    print(df.describe())


def knapsack_optimization(action_list, budget_max):
    """
    Optimises the choice of shares to buy according to the maximum budget.
    Use the Knapsack Problem algorithm to maximise profit.
    """
    price_with_decimal = False
    # Check if any action has a decimal cost
    for action in action_list:
        if isinstance(action.cost, float) and not action.cost.is_integer():
            price_with_decimal = True
            break

    if price_with_decimal:
        budget_max = int(budget_max * 100)
        # costs and profits multiplied by 100
        action_list = [
            Action(
                action.name,
                int(action.cost * 100),
                profit_euros=int(action.profit_euros * 100)
            )
            for action in action_list
        ]

    # Total number of shares
    n = len(action_list)
    print(f"Nombre d'actions : {n}")
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
            profit_previous_action_for_budget = dp[i - 1][budget]
            if cost <= budget:
                # Maximum profit including the current action
                best_profit_action = dp[i - 1][budget - cost]
                dp[i][budget] = max(profit_previous_action_for_budget, best_profit_action + profit)
            else:
                # Maximum profit excluding the current action
                dp[i][budget] = profit_previous_action_for_budget

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

    if price_with_decimal:
        # Convert costs back to euros
        total_cost = round(total_cost / 100, 2)
        # Convert profits back to euros
        total_profit = round(total_profit / 100, 2)

    return selected_actions, total_cost, total_profit


def clean_data(file_path):
    """
    Clean the dataset by removing rows with negative or zero prices.
    """
    # chargement et affichage des données
    data = pd.read_csv(file_path)
    price_count = data['price'].count()
    # Suppression des lignes où price est négatif ou nul
    data = data[data['price'] > 0]
    print(f"Nombre de lignes supprimées (price <= 0) : {price_count - data['price'].count()}")
    # Ajouter une colonne 'benefice_pourcent' pour le calcul du bénéfice
    data['benefice_pourcent'] = data['profit'] / data['price'] * 100
    # Suppression des lignes où benefice_pourcent est supérieur à 50%
    data = data[data['benefice_pourcent'] <= 40]
    return data


def main():
    """
    Main function for running the programme.
    Loads the actions from the CSV files, optimises the backpack and displays
    the results.
    """
    csv_files_names = ["Liste+d'actions+-+P7+Python+-+Feuille+1.csv", "dataset1_Python+P7.csv", "dataset2_Python+P7.csv"]
    max_budget = 500
    # Utilisation de l'optimisation par programmation dynamique
    for csv_file in csv_files_names:
        start_time = time.time()
        # Chemin complet du fichier CSV
        csv_file_path = os.path.join(CSV_FOLDER, csv_file)
        print(f"Traitement du fichier : {csv_file_path}")
        # si le nom du fichier commence par "dataset", on nettoie les données
        if os.path.basename(csv_file_path).startswith("dataset"):
            display_dataframe_overview(pd.read_csv(csv_file_path))
            action_list = load_actions_from(clean_data(csv_file_path))
        else:
            # Chargement des actions depuis le fichier CSV
            action_list = load_actions_from_csv(csv_file_path)
        # Optimisation du sac à dos
        selected_actions, total_cost, total_profit = knapsack_optimization(action_list, max_budget)
        # Affichage des résultats
        print(f"Actions sélectionnées : {', '.join(selected_actions)}")
        print(f"Coût total : {total_cost} €")
        print(f"Bénéfice total : {total_profit:.2f} €")
        execution_time = time.time() - start_time
        print(f"Temps d'exécution : {execution_time:.2f} secondes\n")


if __name__ == "__main__":
    main()
