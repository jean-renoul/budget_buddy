import matplotlib.pyplot as plt
import mysql.connector
from Db import Db


class PieChart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.db = Db("82.165.185.52", "budget-buddy", "database-budget-buddy", "jean-renoul_budget-buddy")

    def calculate_expenses_and_income(self):
        query = "SELECT type, category, SUM(amount) FROM transactions WHERE user_id = %s GROUP BY type, category"
        params = (self.user_id,)
        transactions = self.db.fetch(query, params)

        expenses = {}
        income = {}
        for type, category, amount in transactions:
            if type == "dépense":
                expenses[category] = expenses.get(category, 0) + amount
            elif type == "revenu":
                income[category] = income.get(category, 0) + amount

        return expenses, income

    def plot_pie_chart(self):
        expenses, income = self.calculate_expenses_and_income()

        total_expenses = sum(expenses.values())
        total_income = sum(income.values())

        # Création du diagramme circulaire pour les dépenses
        plt.subplot(1, 2, 1)
        plt.pie(expenses.values(), labels=expenses.keys(), autopct='%1.1f%%', startangle=140)
        plt.title(f"Expenses (Total: {total_expenses})")

        # Création du diagramme circulaire pour les revenus
        plt.subplot(1, 2, 2)
        plt.pie(income.values(), labels=income.keys(), autopct='%1.1f%%', startangle=140)
        plt.title(f"Income (Total: {total_income})")

        plt.show()

if __name__ == "__main__":
    pie_chart = PieChart(6)  # Remplacez par l'ID utilisateur souhaité
    pie_chart.plot_pie_chart()
