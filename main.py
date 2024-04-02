from classes.Back.Connection import Connection
from classes.Front.Login import Login
from classes.Front.Registration import Registration
from classes.Back.Users import Users
from classes.Front.MainPage import MainPage
from classes.Back.Transactions import Transactions
from classes.Front.TransactionPage import TransactionPage
from classes.Front.TransferPage import TransferPage
from classes.Back.Notification import Notification
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

            if self.interface.menu_transactions == True:
                self.interface.menu_transactions = False
                self.transaction_page()

            elif self.interface.menu_transfer == True:
                self.interface.menu_transfer = False
                self.transfer_page()


    def transaction_page(self):
        self.interface = TransactionPage(self.user)
        while True:
            self.interface.run()
            if self.interface.menu_transfer == True:
                self.interface.menu_transfer = False
                self.transfer_page()
            
            elif self.interface.welcome == True:
                self.interface.welcome = False
                self.main_page()

            elif self.interface.sort_by_amount == True:
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

    def transfer_page(self):
        self.interface = TransferPage(self.user)
        while True:
            self.interface.run()

            if self.interface.menu_transactions == True:
                self.interface.menu_transactions = False
                self.transaction_page()

            elif self.interface.welcome == True:
                self.interface.welcome = False
                self.main_page()

            elif self.interface.add_transaction == True:
                transaction = Transactions(self.user.id, self.interface.transfer_data["name"], self.interface.transfer_data["description"], self.interface.transfer_data["category"], self.interface.transfer_data["amount"], self.interface.transfer_data["type"])
                print (transaction.user_id, transaction.name, transaction.description, transaction.category, transaction.amount, transaction.transaction_type)
                print (f"User balance before update : {self.user.balance}")
                transaction.add_transaction()
                self.user.update()
                notification = Notification("Transaction added", "Your transaction has been added successfully")
                notification.send()
                self.interface.add_transaction = False
                

main = Main()
main.user = Users("Doe", "John", "John.Doe@gmail.com", "Password10!")
main.user.update()
main.main_page()

# To uncomment for the real application
#main.login_page()