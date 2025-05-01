import csv
from itertools import combinations


# classe Action
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


def calcule_cout(indices):
    cout_total = 0
    for indice in indices:
        cout_total += actions[indice].cout
    return cout_total


# Chemin vers le fichier CSV
csv_file = "Liste+d'actions+-+P7+Python+-+Feuille+1.csv"
# Liste des actions
actions = load_actions_from_csv(csv_file)
# Affichage des actions
print("Liste des actions :")
for action in actions:
    print(action)
# Indices des actions à combiner
indices = range(0, 9)


def generate_combinations(liste, investissement_max=500):
    combinaisons = []  # Liste pour stocker les combinaisons
    # boucle sur le nombre d'éléments dans chaque combinaison
    for i in range(1, len(liste) + 1):
        # utilise itertools.combinations pour générer les combinaisons
        for combinaison in combinations(liste, i):
            # calcule le coût total de la combinaison
            cout_total = sum(actions[indice].cout for indice in combinaison)
            if cout_total <= investissement_max:
                # Ajoute la combinaison (avec noms des actions) à la liste
                noms_actions = [actions[indice].nom for indice in combinaison]
                benefice = sum(
                    actions[indice].benefice_euros for indice in combinaison
                )
                combinaisons.append((noms_actions, cout_total, benefice))
    return combinaisons  # Retourne la liste des combinaisons


# Appel de la fonction et affichage du résultat
resultat = generate_combinations(indices)
# Trie les résultats par bénéfice décroissant
resultat_trie = sorted(resultat, key=lambda x: x[2], reverse=True)

# Affichage formaté sous forme de tableau
print("Combinaisons d'actions respectant le budget (triées par bénéfice) :")
print(f"{'Actions':<80} {'Coût total (€)':<15} {'Bénéfice (€)':<15}")
print("-" * 110)
for combinaison, cout_total, benefice in resultat_trie:
    actions_str = " ".join(combinaison)
    print(f"{actions_str:<80} {cout_total:<15} {benefice:.2f}".replace('.', ','))
