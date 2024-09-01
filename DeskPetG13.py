import random
import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox


class DeskPetG13(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.easterEgg = []
        self.isDragging = False
        self.isMoving = False
        self.change = False

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(100, 900, 100, 100)
        self.currentAction = self.startIdle
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        self.startIdle()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showMenu)
        self.setMouseTracking(True)
        self.dragging = False
        # Create a QTimer object
        self.popup_timer = QTimer(self)
        # Connect timer to a function
        self.popup_timer.timeout.connect(self.show_popup)

    def loadImages(self, path):
        return [QtGui.QPixmap(os.path.join(path, f)) for f in os.listdir(path) if f.endswith('.png')]

    def startIdle(self):
        self.setFixedSize(400, 200)
        self.currentAction = self.startIdle
        self.images = self.loadImages("DeskPetResources/walk")
        self.currentImage = 0
        self.timer.start(155)

    def updateAnimation(self):
        self.setPixmap(self.images[self.currentImage])
        self.currentImage = (self.currentImage + 1) % len(self.images)

    def showMenu(self, position):
        menu = QtWidgets.QMenu()
        if self.currentAction == self.startIdle:
            self.setMenu(menu, ("Sleep", "Dance", "Exercise", "Eat"))
        elif self.currentAction == self.dance or self.currentAction == self.exercise:
            self.setMenu(menu, ("Sleep", "Eat"))
        else:
            self.setMenu(menu, ("Idle", "Sleep", "Dance", "Exercise", "Eat"))

        menu.exec_(self.mapToGlobal(position))

    def setMenu(self, menu, selected_actions):
        actions = {"Idle": self.startIdle, "Sleep": self.sleep, "Dance": self.dance, "Exercise": self.exercise,
                   "Eat": self.eat}
        for action in selected_actions:
            menu.addAction(action, actions.get(action))
        menu.addSeparator()
        child_menu = menu.addMenu("Easter Egg")
        child_menu.addAction("Developers", self.startEasterEgg)
        menu.addAction("Minimize", self.minimizeWindow)
        menu.addAction("Quit", self.close)

    # implementation for sleep action
    def sleep(self):
        self.setFixedSize(400, 200)
        self.currentAction = self.sleep
        self.images = self.loadImages("DeskPetResources/sleep")
        self.currentImage = 0
        self.timer.start(155)

    # implementation for dance action
    def dance(self):
        self.setFixedSize(400, 200)
        self.currentAction = self.dance
        self.images = self.loadImages("DeskPetResources/dance")
        self.currentImage = 0
        self.timer.start(155)

    # implementation for exercise action
    def exercise(self):
        self.setFixedSize(400, 200)
        self.currentAction = self.exercise
        self.images = self.loadImages("DeskPetResources/exercise")
        self.currentImage = 0
        self.timer.start(155)
        # Set timer to call function after 5 seconds (5000 milliseconds)
        self.popup_timer.singleShot(5000, lambda: self.show_popup(random.choice(["I am tired!","I am hungry!"]),self.exercise))

    # implementation for eat action
    def eat(self):
        self.setFixedSize(400, 200)
        self.currentAction = self.eat
        self.images = self.loadImages("DeskPetResources/eat")
        self.currentImage = 0
        self.timer.start(155)
        # Set timer to call function after 5 seconds (5000 milliseconds)
        self.popup_timer.singleShot(5000, lambda: self.show_popup("I am full!",self.eat))

    def show_popup(self, message, currentAction):
        if self.currentAction == currentAction:
            msg = QMessageBox(self)
            msg.setWindowTitle("Alert")
            msg.setText(message)
            msg.exec_()
        else:
            print("Action has changed, stopped showing popup.")

    def startEasterEgg(self):
        easterEgg = EasterEgg()
        easterEgg.show()
        self.easterEgg.clear()
        self.easterEgg.append(easterEgg)

    def closeEvent(self, event):
        for child in self.easterEgg:
            child.close()
        super().closeEvent(event)

    def minimizeWindow(self):
        self.showMinimized()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.isDragging = True
            self.drag_position = event.globalPos() - self.pos()
            self.prevAction = self.currentAction
            event.accept()

    def mouseMoveEvent(self, event):
        if QtCore.Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False
            self.isDragging = False
            self.prevAction()  # 或者 self.startIdle(), 根据之前的动作恢复状态
            event.accept()


class EasterEgg(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Easter Egg')
        self.setGeometry(400, 900, 100, 100)
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Group 13 Python Programming project")
        label.setAlignment(QtCore.Qt.AlignCenter)
        description = QtWidgets.QLabel("Lin Yuqing\nLiu Zigen\nChen Shulin\nChen Zi\nDing Haoxuan")
        description.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(description)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(layout)

app = QtWidgets.QApplication(sys.argv)
pet = DeskPetG13()
pet.show()
easter_egg = EasterEgg()
sys.exit(app.exec_())
