import csv


# classe Action
class Action:
    def __init__(self, nom, cout, benefPourcent):
        self.nom = nom
        self.cout = cout
        self.benefPourcent = benefPourcent

    def __str__(self):
        return f"Action({self.nom}, {self.cout}, {self.benefPourcent})"


def load_actions_from_csv(file_path):
    """
    Charge les actions à partir d'un fichier CSV.

    Chaque ligne du fichier CSV est convertie en une instance de la classe Action.
    Les colonnes attendues dans le fichier sont :
    - 'Nom' : le nom de l'action
    - 'Coût' : le coût de l'action (converti en entier)
    - 'Bénéfice (%)' : le pourcentage de bénéfice (le symbole '%' est supprimé et converti en entier)

    :param file_path: Chemin vers le fichier CSV
    :return: Liste d'objets Action
    """
    actions = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        print("Contenu du fichier CSV :")
        for row in reader:
            # Création d'une instance de la classe Action pour chaque ligne
            # supprime le % de la colonne Bénéfice (%)
            # et convertit en entier
            action = Action(
                nom=row['Nom'],
                cout=int(row['Coût']),
                benefPourcent=int(row['Bénéfice (%)'].replace('%', ''))
            )
            # Ajout de l'action à la liste
            actions.append(action)
    return actions


# Chemin vers le fichier CSV
csv_file = "Liste+d'actions+-+P7+Python+-+Feuille+1.csv"
# Liste des actions
actions = load_actions_from_csv(csv_file)
