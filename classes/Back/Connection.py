from classes.Back.Db import Db
from classes.Back.Users import Users
import string

class Connection:
    def __init__(self, lastname, firstname, email, password):
        self.lastname = lastname
        self.firstname = firstname
        self.email = email
        self.password = password
        self.db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")
        self.error = ""

    def password_verification(self):
        if self.check_password_size() and self.check_password_number() and self.check_password_uppercase() and self.check_password_lowercase() and self.check_password_special_character():
            print ("Password is valid")
            return True
        else:
            print ("Password is invalid")
            return False

    def check_password_size(self):
        if len(self.password) >= 10:
            return True
        else:
            print ("Password does not have enough characters")
            self.error = "Password does not have enough characters"
            return False
        
    def check_password_number(self):
        if any(char.isdigit() for char in self.password):
            return True
        else:
            print ("Password does not have a number")
            self.error = "Password does not have a number"
            return False
        
    def check_password_uppercase(self):
        if any(char.isupper() for char in self.password):
            return True
        else:
            print ("Password does not have an uppercase letter")
            self.error = "Password does not have an uppercase letter"
            return False
        
    def check_password_lowercase(self):
        if any(char.islower() for char in self.password):
            return True
        else:
            print ("Password does not have a lowercase letter")
            self.error = "Password does not have a lowercase letter"
            return False
        
    def check_password_special_character(self):
        if any(char in string.punctuation for char in self.password):
            return True
        else:
            print ("Password does not have a special character")
            self.error = "Password does not have a special character"
            return False
        
    def check_existing_email(self):
        query = "SELECT * FROM users WHERE email = %s"
        params = (self.email,)
        result = self.db.fetch(query, params)
        if result:
            print ("Email already exists")
            self.error = "Email already exists"
            return True
        else:
            return False
        
    def check_existing_password(self):
        query = "SELECT * FROM users WHERE password = %s"
        params = (self.password,)
        result = self.db.fetch(query, params)
        if result:
            print ("Password already exists")
            self.error = "Password already exists"
            return True
        else:
            return False
        
    def check_existing_user(self):
        if self.check_existing_email() or self.check_existing_password():
            self.error = "User already exists"
            return True
        else:
            return False
        
    def register(self):
        if self.password_verification() and not self.check_existing_user():
            self.user = Users(self.lastname, self.firstname, self.email, self.password)
            query = "INSERT INTO users (lastname, firstname, email, password, balance) VALUES (%s, %s, %s, %s, %s)"
            params = (self.user.last_name, self.user.first_name, self.user.email, self.user.password, self.user.balance)
            self.db.executeQuery(query, params)

    def login(self):
        query = "SELECT * FROM users WHERE lastname = %s AND firstname = %s AND email = %s AND password = %s"
        params = (self.lastname, self.firstname, self.email, self.password)
        result = self.db.fetch(query, params)
        if result:
            print ("User found")
            self.user = Users(result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])
            return True
        else:
            print ("User not found")
            return False


if __name__ == "__main__":
    connection = Connection("Doe", "John", "John.Doe@gmail.com", "Password10!")
    print (connection.login())