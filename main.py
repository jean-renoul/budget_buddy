from classes.Back.Connection import Connection
from classes.Front.Login import Login
from classes.Front.registration import Registration
from classes.Back.Users import Users
from classes.Front.MainPage import MainPage
import pygame

pygame.init()

class Main:

    def __init__(self):
        self.user = None
        self.interface = None

    def login_page(self):
        self.interface = Login()
        while True:
            self.interface.run()

            if self.interface.login_attempt:
                connection = Connection(self.interface.form_data["Lastname"], self.interface.form_data["Firstname"], self.interface.form_data["Email"], self.interface.form_data["Password"])
                if connection.login():
                    self.interface.login_attempt = False
                    self.interface.message("Login successful")
                    self.user = Users(self.interface.form_data["Lastname"], self.interface.form_data["Firstname"], self.interface.form_data["Email"], self.interface.form_data["Password"])
                    self.user.update()
                    self.main_page()
                else:
                    self.interface.message("Login failed")
                    self.interface.login_attempt = False
            if self.interface.register:
                self.interface.register = False
                self.registration_page()

    def registration_page(self):
            self.interface = Registration()
            while True:
                self.interface.run()
                if self.interface.back_to_login:
                    self.interface.back_to_login = False
                    self.login_page()
                if self.interface.registration_attempt:
                    connection = Connection(self.interface.form_data["Lastname"], self.interface.form_data["Firstname"], self.interface.form_data["Email"], self.interface.form_data["Password"])
                    if connection.register():
                        self.interface.registration_attempt = False
                        self.interface.message("Registration successful")
                    else:
                        self.interface.message(connection.error)
                        self.interface.registration_attempt = False

    def main_page(self):
        self.interface = MainPage(self.user)
        while True:
            self.interface.run()

            if self.interface.sort_by_amount == True:
                self.user.sort_transactions_by_amount()
                self.interface.sort_by_amount = False
                self.interface.transactions = self.user.transactions

            elif self.interface.sort_by_date == True:
                self.user.sort_transactions_by_date()
                self.interface.sort_by_date = False
                self.interface.transactions = self.user.transactions

            elif self.interface.sort_by_category == True:
                self.user.sort_transactions_by_category()
                self.interface.sort_by_category = False
                self.interface.transactions = self.user.transactions

            elif self.interface.sort_by_type == True:
                self.user.sort_transactions_by_type()
                self.interface.sort_by_type = False
                self.interface.transactions = self.user.transactions

main = Main()
main.user = Users("Doe", "John", "John.Doe@gmail.com", "Password10!")
main.user.update()
main.main_page()

# To uncomment for the real application
#main.login_page()