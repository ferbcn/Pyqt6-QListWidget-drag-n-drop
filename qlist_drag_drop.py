
import sys

from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QListWidget, QListWidgetItem, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt5.Qt import QApplication
from PyQt5.QtCore import QObject, pyqtSignal

class ThumbListWidget(QListWidget):

    def __init__(self, type, parent=None):
        super(ThumbListWidget, self).__init__(parent)
        self.setIconSize(QtCore.QSize(124, 124))
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(ThumbListWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            super(ThumbListWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        #print('dropEvent', event)
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))

        else:
            event.setDropAction(QtCore.Qt.MoveAction)
            super(ThumbListWidget, self).dropEvent(event)


class Window(QMainWindow):

    trigger = pyqtSignal ()

    def __init__(self):
        super(QMainWindow,self).__init__()
        self.listItems={}

        myQWidget = QWidget()
        self.setCentralWidget(myQWidget)

        myBoxLayout = QVBoxLayout()
        self.listWidgetA = ThumbListWidget(self)
        self.listWidgetA.setAcceptDrops (False)
        #self.listWidgetA.setAlternatingRowColors (True)
        for i in range(12):
            item = QListWidgetItem( 'Item '+str(i), self.listWidgetA )
        myBoxLayout.addWidget(self.listWidgetA)

        self.listWidgetB = ThumbListWidget(self)
        myBoxLayout.addWidget(self.listWidgetB)
        self.listWidgetB.setAcceptDrops (True)

        # create widgets
        delButton = QPushButton ("Delete Item")
        clrButton = QPushButton ("Clear List ")
        saveButton = QPushButton ("Save List  ")

        # define layout: a horizontal box with three buttons in it
        hbox = QHBoxLayout ()
        hbox.addWidget (delButton)
        hbox.addWidget (clrButton)
        hbox.addWidget (saveButton)
        hbox.setContentsMargins (0, 0, 0, 0)

        myBoxLayout.addLayout(hbox)
        myQWidget.setLayout(myBoxLayout)

        # connect button to methods on_click
        delButton.clicked.connect (self.deleteItem)
        clrButton.clicked.connect (self.clearList)
        saveButton.clicked.connect (self.saveList)

        #self.connect(self.listWidgetA, QtCore.SIGNAL("dropped"), self.items_dropped)
        #self.trigger.connect(self.items_dropped)
        self.listWidgetA.currentItemChanged.connect(self.item_clicked)
        self.listWidgetB.currentItemChanged.connect(self.item_clicked)

    def items_dropped(self, arg):
        pass #print ('items_dropped', arg)

    def item_clicked(self, arg):
        pass #print (arg)

    def deleteItem(self):
        listItems = self.listWidgetB.selectedItems()
        if not listItems:
            self.listWidgetB.setCurrentItem (self.listWidgetB.item (0))
            if self.listWidgetB.count()ß > 0:
                self.deleteItem()
        for item in listItems:
            self.listWidgetB.takeItem(self.listWidgetB.row(item))

    def clearList(self):
        self.listWidgetB.setCurrentItem(self.listWidgetB.item(0))
        for i in range(self.listWidgetB.count()):
            self.listWidgetB.clear()

    def saveList (self):
        num_items = self.listWidgetB.count ()
        list2save = []
        for i in range (num_items):
            list2save.append(self.listWidgetB.item(i).text())
        print (list2save)
        #TO-DO: do something with the list


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = Window()
    myapp.show()
    myapp.resize(480,320)
    sys.exit(app.exec_())