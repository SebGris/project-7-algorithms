import csv
import time


class Action:
    def __init__(self, name, cost, benefice_pourcent):
        self.name = name
        self.cost = cost
        self.benefice_pourcent = benefice_pourcent
        self.benefice_euros = round(cost * (benefice_pourcent / 100), 2)


def load_actions_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        return [
            Action(
                name=row['Actions #'],
                cost=int(row['Coût par action (en euros)']),
                benefice_pourcent=int(row['Bénéfice (après 2 ans)'].replace('%', ''))
            )
            for row in csv.DictReader(file)
        ]


def greedy_selection(action_list, budget_max):
    # Vérifie si la liste des actions est vide ou si le budget est invalide
    if not action_list or budget_max <= 0:
        return [], 0, 0

    # Trie les actions par ratio profit-coût en ordre décroissant
    action_list.sort(key=lambda x: x.benefice_pourcent, reverse=True)

    selected_actions = []  # Liste pour stocker les actions sélectionnées
    total_profit = 0       # Profit total des actions sélectionnées
    budget = 0             # Budget utilisé

    # Itère sur chaque action triée
    for action in action_list:
        cost = action.cost
        profit = action.benefice_euros

        # Ajoute l'action si elle ne dépasse pas le budget restant
        if cost + budget <= budget_max:
            selected_actions.append(action.name)
            budget += cost
            total_profit += profit
        else:
            break  # Arrête l'itération si l'action dépasse le budget

    # Retourne les actions sélectionnées, le budget utilisé et le profit total
    return selected_actions, budget, total_profit



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
    selected_actions, total_cost, total_profit = greedy_selection(action_list, max_budget)
    combinations_generation_time = time.time() - start_time
    print(f"Temps d'exécution : {combinations_generation_time:.2f} secondes")
    # Écriture des résultats dans un fichier
    output_file = "resultat_glouton.txt"
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
