import csv
from itertools import combinations
from tqdm import tqdm
import time  # Importation du module time pour mesurer le temps d'exécution


class Action:
    def __init__(self, nom, cout, benefPourcent):
        self.nom = nom
        self.cout = cout
        self.benefPourcent = benefPourcent

    @property
    def benefice_euros(self):
        """
        Calcule le bénéfice en euros basé sur le coût
        et le pourcentage de bénéfice.
        """
        return round(self.cout * (self.benefPourcent / 100), 2)

    def __str__(self):
        return (
            f"Action({self.nom}, {self.cout}, {self.benefPourcent}, "
            f"{self.benefice_euros})"
        )


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


# Chemin vers le fichier CSV
csv_file = "Liste+d'actions+-+P7+Python+-+Feuille+1.csv"
# Liste des actions
actions = load_actions_from_csv(csv_file)


def generate_combinations(actions, investissement_max=500):
    """
    Génère toutes les combinaisons possibles d'actions respectant le budget.

    :param actions: Liste d'objets Action
    :param investissement_max: Budget maximum (en euros)
    :return: Liste des combinaisons sous forme de tuples
             (noms_actions, cout_total, benefice)
    """
    combinaisons = []  # Liste pour stocker les combinaisons
    total_combinations = sum(
        len(list(combinations(actions, i))) for i in range(1, len(actions) + 1)
    )
    # Utilisation de tqdm pour afficher la progression
    with tqdm(
        total=total_combinations,
        desc="Génération des combinaisons"
    ) as pbar:
        for i in range(1, len(actions) + 1):
            for combinaison in combinations(actions, i):
                cout_total = sum(action.cout for action in combinaison)
                if cout_total <= investissement_max:
                    noms_actions = [action.nom for action in combinaison]
                    benefice = sum(
                        action.benefice_euros for action in combinaison
                    )
                    combinaisons.append((noms_actions, cout_total, benefice))
                pbar.update(1)  # Mise à jour de la jauge d'avancement
    return combinaisons  # Retourne la liste des combinaisons


# Mesure du temps d'exécution
start_time = time.time()
resultat = generate_combinations(actions)
print(f"Nombre total de combinaisons générées : {len(resultat)}")
combinations_generation_time = time.time() - start_time
print(f"Temps d'exécution : {combinations_generation_time:.2f} secondes")
# Trie les résultats par bénéfice décroissant
resultat_trie = sorted(resultat, key=lambda x: x[2], reverse=True)
# Affichage formaté sous forme de tableau
output_file = "resultat_combinations.txt"
with open(output_file, mode="w", encoding="utf-8") as file:
    header = f"{'Actions':<145} {'Coût total (€)':<15} {'Bénéfice (€)':<15}\n"
    separator = "-" * 175 + "\n"
    file.write(
        "Combinaisons d'actions respectant le budget "
        "(triées par bénéfice) :\n"
    )
    file.write(header)
    file.write(separator)
    # Ajout de la jauge de progression pour l'écriture
    with tqdm(
        total=len(resultat_trie),
        desc="Écriture dans le fichier"
    ) as pbar:
        for noms_actions, cout_total, benefice in resultat_trie:
            actions_str = " ".join(noms_actions)
            formatted_line = (
                f"{actions_str:<145} {cout_total:<15} {benefice:.2f}"
            ).replace('.', ',')
            file.write(formatted_line + "\n")
            pbar.update(1)  # Mise à jour de la jauge d'avancement

execution_time = time.time() - start_time - combinations_generation_time
print(f"Temps d'exécution : {execution_time:.2f} secondes")
# Calcul et affichage du temps d'exécution
execution_time = time.time() - start_time
print(f"Résultat écrit dans le fichier : {output_file}")
print(f"Temps d'exécution total : {execution_time:.2f} secondes")
