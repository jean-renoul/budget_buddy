from classes.Connection import Connection
from classes.interface import Interface
import threading

interface_connection = Interface()

def handle_connection_attempt():
    while True:
        if interface_connection.login_attempt:
            connection = Connection(interface_connection.form_data["Lastname"], interface_connection.form_data["Firstname"], interface_connection.form_data["Email"], interface_connection.form_data["Password"])
            if connection.login():
                interface_connection.login_attempt = False
                interface_connection.message("Login successful")
            else:
                interface_connection.message("Login failed")
                interface_connection.login_attempt = False


thread = threading.Thread(target=handle_connection_attempt)
thread.start()
interface_connection.run()