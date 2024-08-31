import sys
import os
import random
from PyQt5 import QtWidgets, QtGui, QtCore


class DeskPetG13(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.childPets = []
        self.isDragging = False
        self.isMoving = False
        self.change = False

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(500, 500, 130, 130)
        self.currentAction = self.startIdle
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        # self.changeDirectionTimer = QtCore.QTimer(self)  # 添加定时器
        # self.changeDirectionTimer.timeout.connect(self.changeDirection)  # 定时器触发时调用changeDirection方法
        self.startIdle()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showMenu)
        self.setMouseTracking(True)
        self.dragging = False

    def loadImages(self, path):
        return [QtGui.QPixmap(os.path.join(path, f)) for f in os.listdir(path) if f.endswith('.png')]

    def startIdle(self):
        self.setFixedSize(400, 200)
        self.currentAction = self.startIdle
        self.images = self.loadImages("DeskPetResources/walk")
        self.currentImage = 0
        self.timer.start(95)
        self.moveSpeed = 0
        self.movingDirection = 0

    def updateAnimation(self):
        self.setPixmap(self.images[self.currentImage])
        self.currentImage = (self.currentImage + 1) % len(self.images)

    def showMenu(self, position):
        menu = QtWidgets.QMenu()
        if self.currentAction == self.startIdle:
            # menu.addAction("Sleep", self.Sleep)
            # menu.addAction("Dance", self.Dance)
            # menu.addAction("Exercise", self.Exercise)
            # menu.addAction("Eat", self.Eat)
            menu.addSeparator()
            child_menu = menu.addMenu("Easter Egg")
            child_menu.addAction("Developers", self.startEasterEgg)
            menu.addAction("Minimize", self.minimizeWindow)
            menu.addAction("Quit", self.close)
        else:
            # menu.addAction("Sleep", self.Sleep)
            # menu.addAction("Dance", self.Dance)
            # menu.addAction("Exercise", self.Exercise)
            # menu.addAction("Eat", self.Eat)
            menu.addSeparator()
            child_menu = menu.addMenu("Easter Egg")
            child_menu.addAction("Developers", self.startEasterEgg)
            menu.addAction("Minimize", self.minimizeWindow)
            menu.addAction("Quit", self.close)
        menu.exec_(self.mapToGlobal(position))

    # TODO: implementation for sleep action
    # def Sleep(self):

    # TODO: implementation for dance action
    # def Dance(self):

    # TODO: implementation for exercise action
    # def Exercise(self):

    # TODO: implementation for sleep action
    # def Eat(self):

    def startEasterEgg(self):
        easterEgg = EasterEgg()
        easterEgg.show()
        self.childPets.append(easterEgg)

    def closeEvent(self, event):
        for child in self.childPets:
            child.close()  # 关闭所有子窗口
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
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Group 13 Python Programming project")
        label.setAlignment(QtCore.Qt.AlignCenter)
        description = QtWidgets.QLabel("Lin Yuqing\nLiu Zigen\nChen Shulin\nChen Zi\nDing Haoxuan")
        description.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(description)

        self.new_window = None  # 新窗口实例作为成员变量
        self.setLayout(layout)


app = QtWidgets.QApplication(sys.argv)
pet = DeskPetG13()
pet.show()
easter_egg = EasterEgg()
sys.exit(app.exec_())
