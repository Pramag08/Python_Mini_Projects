from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QListWidget, QComboBox, QLineEdit, QDateEdit, QTableWidget, QMessageBox, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtCore import Qt, QDate
import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(650, 500)
        self.setWindowTitle('Expense Tracker')

        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.add_button = QPushButton('Add Expense')
        self.delete_button = QPushButton('Delete Expense')
        self.add_button.clicked.connect(self.add_expense)
        self.delete_button.clicked.connect(self.delete_expense)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Id", "Date", "Category", "Amount", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.sortByColumn(1, Qt.DescendingOrder)
         

        self.dropdown.addItems(["Food", "Transport", "Rent", "Entertainment", "Bills", "Shopping", "Medical", "Others"]) 

        self.setStyleSheet("""
            QWidget {background-color: #b8c9e1;}

            Qlabel {
            color:#333;
            font-size: 14px;}

            QLineEdit , QComboBox, QDateEdit {background-color: #b8c9e1; color:#333; border: 1px solid #444; 
            border-radius: 5px; padding: 5px;}

            QPushButton {background-color: #4CAF50; color: white; border: none; border-radius: 5px; padding: 8px 16px; font-size: 14px;}

            QPushButton:hover {background-color: #45a049;}

            QTableWidget {background-color: #b8c9e1; color: #333; border: 1px solid black; border-radius: 5px; selection-background-color:#ddd;}




        """)

        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        self.row1.addWidget(QLabel('Date'))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel('Category'))
        self.row1.addWidget(self.dropdown)

        self.row2.addWidget(QLabel('Amount'))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel('Description'))
        self.row2.addWidget(self.description)

        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.delete_button)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)

        self.master_layout.addWidget(self.table)

        self.setLayout(self.master_layout)

        self.load_table()

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Select a row to delete expense!")
            return
        expense_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self, "Delete Expense", "Are you sure you want to delete this expense?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.No:
            return
        query = QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = ?")
        query.addBindValue(expense_id)
        query.exec_()

        self.load_table()




    def load_table(self):
        self.table.setRowCount(0)

        query = QSqlQuery("SELECT * FROM expenses")
        row = 0
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)

            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 4, QTableWidgetItem(description))

            row += 1

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        query = QSqlQuery()
        query.prepare(
            """INSERT INTO expenses(date, category, amount, description) 
                VALUES(?, ?, ?, ?)""")
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()

        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

        self.load_table()


database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expense.db")
if not database.open():
    QMessageBox.critical(None, "Error", "Database Connection Error:")
    sys.exit(1)

query = QSqlQuery()
query.exec_(
    """CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, category TEXT, amount REAL, description TEXT)""")

if __name__ == "__main__":
    app = QApplication([])
    main_window = ExpenseTracker()
    main_window.show()
    app.exec_()
