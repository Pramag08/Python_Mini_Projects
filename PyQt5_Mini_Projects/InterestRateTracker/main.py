import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTreeView, QMessageBox, QHeaderView, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class FinanceApp(QMainWindow):
    def __init__(self):
        super(FinanceApp, self).__init__()
        self.setWindowTitle("Interest Rate Tracker")
        self.resize(900, 700)

        main_window = QWidget()

        self.rate_label = QLabel("Interest Rate(%):")
        self.rate_input = QLineEdit()

        self.initial_label = QLabel("Initial Investment:")
        self.initial_input = QLineEdit()

        self.years_label = QLabel("Years to Invest:")
        self.years_input = QLineEdit()

        self.model = QStandardItemModel()
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["Year", "Total Investment"])
        self.tree.header().setSectionResizeMode(QHeaderView.Stretch)

        self.calc_button = QPushButton("Calculate")
        self.clear_button = QPushButton("Clear")
        self.save_button = QPushButton("Save")

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()

        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()

        self.row1.addWidget(self.rate_label)
        self.row1.addWidget(self.rate_input)
        self.row1.addWidget(self.initial_label)
        self.row1.addWidget(self.initial_input)
        self.row1.addWidget(self.years_label)
        self.row1.addWidget(self.years_input)

        self.col1.addWidget(self.tree)
        self.col1.addWidget(self.calc_button)
        self.col1.addWidget(self.clear_button)
        self.col1.addWidget(self.save_button)

        self.col2.addWidget(self.canvas)

        self.row2.addLayout(self.col1, 30)
        self.row2.addLayout(self.col2, 70)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)

        main_window.setLayout(self.master_layout)
        self.setCentralWidget(main_window)

        self.calc_button.clicked.connect(self.calc_interest)
        self.clear_button.clicked.connect(self.reset)
        self.save_button.clicked.connect(self.save_data)

    def calc_interest(self):
        try:
            interest_rate = float(self.rate_input.text())
            initial_investment = float(self.initial_input.text())
            num_years = int(self.years_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid input, please enter a number!")
            return

        total = initial_investment
        self.model.setRowCount(0)  
        for year in range(1, num_years + 1):
            total += total * (interest_rate / 100)
            item_year = QStandardItem(str(year))
            item_total = QStandardItem("{:.2f}".format(total))
            self.model.appendRow([item_year, item_total])

        self.figure.clear()
        ax = self.figure.add_subplot()
        years = list(range(1, num_years + 1))
        totals = [initial_investment * (1 + interest_rate / 100) ** year for year in years]

        ax.plot(years, totals)
        ax.set_title("Interest Chart")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total")
        self.canvas.draw()

    def save_data(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if dir_path:
            folder_path = os.path.join(dir_path, 'Saved')
            os.makedirs(folder_path, exist_ok=True)

            file_path = os.path.join(folder_path, 'result.csv')
            with open(file_path, "w") as file:
                file.write('Year,Total\n')
                for row in range(self.model.rowCount()):
                    year = self.model.index(row, 0).data()
                    total = self.model.index(row, 1).data()
                    file.write(f'{year},{total}\n')
            plt.savefig(os.path.join(folder_path, "chart.png"))

            QMessageBox.information(self, "Success", "Data saved successfully!")
        else:
            QMessageBox.warning(self, "Error", "No directory selected!")

    def reset(self):
        self.rate_input.clear()
        self.initial_input.clear()
        self.years_input.clear()
        self.model.setRowCount(0)
        self.figure.clear()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceApp()
    window.show()
    sys.exit(app.exec_())
