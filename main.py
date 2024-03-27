from classes.Connection import Connection
from classes.Login import Login
from classes.Registration import Registration
import pygame

pygame.init()

def login_page():
    interface = Login()
    while True:
        interface.run()

        if interface.login_attempt:
            connection = Connection(interface.form_data["Lastname"], interface.form_data["Firstname"], interface.form_data["Email"], interface.form_data["Password"])
            if connection.login():
                interface.login_attempt = False
                interface.message("Login successful")
            else:
                interface.message("Login failed")
                interface.login_attempt = False
        if interface.register:
            interface.register = False
            registration_page()

def registration_page():
        interface = Registration()
        while True:
            interface.run()
            if interface.back_to_login:
                interface.back_to_login = False
                login_page()
            if interface.registration_attempt:
                connection = Connection(interface.form_data["Lastname"], interface.form_data["Firstname"], interface.form_data["Email"], interface.form_data["Password"])
                if connection.register():
                    interface.registration_attempt = False
                    interface.message("Registration successful")
                else:
                    interface.message(connection.error)
                    interface.registration_attempt = False

login_page()