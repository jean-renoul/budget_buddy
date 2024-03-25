from classes.Connection import Connection

connection = Connection("Doe", "John", "John.Doe@gmail.com", "Password10!")

if connection.login():
    print(connection.user.first_name, connection.user.last_name)

connection = Connection("Jean", "Renoul", "jean.renoul@laplateforme.io", "Bonpassword1!")

connection.login()
connection.register()