import mysql.connector
class Transactions:
    def __init__(self, name, date, category, description, amount, type):
        self.name = name
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount
        self.type = type

    def add_transaction(self):
        try:
            connexion = mysql.connector.connect(
                host ="82.165.185.52",
                port="3306",
                user ="budget-buddy",
                password="database-budget-buddy",
                database ="jean-renoul_budget-buddy"
            )
            if connexion.is_connected():
                print("conneté à la base de donnée!")

                cursor = connexion.cursor()
                # Validation des données
                if self.amount <= 0:
                        print("Le montant de la transaction doit être positif.")
                        return False
                if self.type not in ['dépense', 'revenu']:
                        print("Le type de transaction doit être 'dépense' ou 'revenu'.")
                        return False

                    # Ajout de la transaction dans la base de données
                cursor.execute("INSERT INTO transactions (name, date, category, description, amount, type) VALUES (%s, %s, %s, %s, %s, %s)",
                                (self.name, self.date, self.category, self.description, self.amount, self.type))
                connexion.commit()

                print("La transaction a été ajoutée avec succès.")
                return True

        except mysql.connector.Error as e:
            print("Erreur lors de l'ajout de la transaction :", e)
            return False

        finally:
            # Fermeture de la connexion à la base de données
            if 'conn' in locals() and connexion.is_connected():
                connexion.close()
                print("Connexion à la base de données fermée.")

# Exemple d'utilisation
name = "Nouvelle transaction"
date = "2024-03-25"
category = "Alimentation"
description = "Achat au supermarché"
amount = 50.00
type = "dépense"

new_transaction = Transactions(name, date, category, description, amount, type)
new_transaction.add_transaction()
            
        
