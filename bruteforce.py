import csv


# classe Action
class Action:
    def __init__(self, nom, cout, benefPourcent):
        self.nom = nom
        self.cout = cout
        self.benefPourcent = benefPourcent

    @property
    def benefice_euros(self):
        """
        Calcule le bénéfice en euros basé sur le coût et le pourcentage de bénéfice.
        """
        return round(self.cout * (self.benefPourcent / 100), 2)

    def __str__(self):
        return f"Action({self.nom}, {self.cout}, {self.benefPourcent}, {self.benefice_euros})"


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

# Affichage des actions
print("Liste des actions :")
for action in actions:
    print(action)
