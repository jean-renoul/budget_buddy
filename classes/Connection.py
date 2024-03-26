from Db import Db
from Users import Users
import string

class Connection:
    def __init__(self, lastname, firstname, email, password):
        self.lastname = lastname
        self.firstname = firstname
        self.email = email
        self.password = password
        self.db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "budget-buddy")

    def password_verification(self):
        if len(self.user.password) >= 10:
            print ("Password has enough characters")
            if any(char.isdigit() for char in self.user.password):
                print ("Password has a number")
                if any(char.isupper() for char in self.user.password):
                    print ("Password has an uppercase letter")
                    if any(char.islower() for char in self.user.password):
                        print ("Password has a lowercase letter")
                        if any(char in string.punctuation for char in self.user.password):
                            print ("Password has a special character")
                            return True
                        else:
                            print ("Password does not have a special character")
                    else:
                        print ("Password does not have a lowercase letter")
                else:
                    print ("Password does not have an uppercase letter")

    def check_password_size(self):
        if len(self.user.password) >= 10:
            print ("Password has enough characters")
            return True
        else:
            print ("Password does not have enough characters")
            return False
        
    def check_password_number(self):
        if any(char.isdigit() for char in self.user.password):
            print ("Password has a number")
            return True
        else:
            print ("Password does not have a number")
            return False
        
    def check_password_uppercase(self):
        if any(char.isupper() for char in self.user.password):
            print ("Password has an uppercase letter")
            return True
        else:
            print ("Password does not have an uppercase letter")
            return False
        
    def check_password_lowercase(self):
        if any(char.islower() for char in self.user.password):
            print ("Password has a lowercase letter")
            return True
        else:
            print ("Password does not have a lowercase letter")
            return False
        
    def check_password_special_character(self):
        
        


if __name__ == "__main__":
    user = Users("Doe", "John", "John.Doe@gmail.com", "Password10")
    connection = Connection(user)
    print (connection.password_verification())