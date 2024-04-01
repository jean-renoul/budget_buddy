from Db import Db

# Définition de la méthode change_password
def change_password(db, user_id, old_password, new_password):
    query = "UPDATE users SET password = %s WHERE user_id = %s AND password = %s"
    params = (new_password, user_id, old_password)
    db.executeQuery(query, params)


# Création d'une instance de Db
db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")

# Utilisation de la méthode change_password
user_id = 8
old_password = "Aaaaaaaaaa1!"
new_password = "iiiiiiiiiiiii1"
change_password(db, user_id, old_password, new_password)
