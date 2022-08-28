import sys

from PyQt6.QtWidgets import (QApplication, QListWidgetItem, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton)
from qlist_drag_drop import ThumbListWidget


class Window(QWidget):
    
    def __init__(self):
        super(QWidget, self).__init__()
        self.listItems = {}

        # Main layout: vertical
        main_layout = QVBoxLayout()
        
        # first list
        self.listWidgetA = ThumbListWidget(self)
        self.listWidgetA.setAcceptDrops(False)
        for i in range(12):
            QListWidgetItem('Item ' + str(i), self.listWidgetA)
        main_layout.addWidget(self.listWidgetA)
        # second list
        self.listWidgetB = ThumbListWidget(self)
        main_layout.addWidget(self.listWidgetB)
        self.listWidgetB.setAcceptDrops(True)

        # buttons
        delButton = QPushButton("Delete Item")
        clrButton = QPushButton("Clear List ")
        saveButton = QPushButton("Save List  ")

        # add buttons to a horizontal layout
        hbox = QHBoxLayout()
        hbox.addWidget(delButton)
        hbox.addWidget(clrButton)
        hbox.addWidget(saveButton)
        hbox.setContentsMargins(0, 0, 0, 0)
        # and add it to main layout 
        main_layout.addLayout(hbox)
        self.setLayout(main_layout)

        # connect button to methods on_click
        delButton.clicked.connect(self.deleteItem)
        clrButton.clicked.connect(self.clearList)
        saveButton.clicked.connect(self.saveList)

        self.listWidgetA.currentItemChanged.connect(self.item_clicked)
        self.listWidgetB.currentItemChanged.connect(self.item_clicked)

    def item_clicked(self, arg):
        # print(arg)
        pass

    def deleteItem(self):
        listItems = self.listWidgetB.selectedItems()
        if not listItems:
            self.listWidgetB.setCurrentItem(self.listWidgetB.item(0))
            if self.listWidgetB.count() > 0:
                self.deleteItem()
        for item in listItems:
            self.listWidgetB.takeItem(self.listWidgetB.row(item))

    def clearList(self):
        self.listWidgetB.setCurrentItem(self.listWidgetB.item(0))
        for i in range(self.listWidgetB.count()):
            self.listWidgetB.clear()

    def saveList(self):
        num_items = self.listWidgetB.count()
        list2save = []
        for i in range(num_items):
            list2save.append(self.listWidgetB.item(i).text())
        print(list2save)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = Window()
    myapp.show()
    myapp.resize(480, 320)
    sys.exit(app.exec())
