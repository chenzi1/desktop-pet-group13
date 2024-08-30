import random
import sys
import os
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

    def startIdle(self):
        self.setFixedSize(130, 130)
        self.currentAction = self.startIdle
        self.images = self.loadImages("DeskPetResources/walk")
        self.currentImage = 0
        self.timer.start(100)
        self.moveSpeed = 0
        self.movingDirection = 0
        # if self.changeDirectionTimer.isActive():
        #     self.changeDirectionTimer.stop()  # 停止方向改变的定时器

    def loadImages(self, path):
        return [QtGui.QPixmap(os.path.join(path, f)) for f in os.listdir(path) if f.endswith('.png')]

    def updateAnimation(self):
        # self.label.setPixmap(self.images[self.currentImage])
        self.currentImage = (self.currentImage + 1) % len(self.images)

    def changeDirection(self):
        if self.currentAction == self.startFall or self.currentAction == self.eating or self.currentAction == self.transform or self.currentAction == self.sleep or self.currentAction == self.pipi or self.currentAction == self.exercise or self.currentAction == self.WakeUp or self.currentAction == self.startIdle or self.startMeet:
            return  # 如果正在执行下落动作，不改变方向

        if random.random() < 0.5:  # 随机选择是否改变方向
            self.movingDirection *= -1
            self.change = True
            if self.change == True:
                # 停止加载原先的图片
                self.timer.stop()
                self.images = []  # 清空当前图片列表
                self.startWalk()
                self.change = False

    def showMenu(self, position):
        menu = QtWidgets.QMenu()
        menu.addAction("隐藏", self.minimizeWindow)
        menu.addAction("回去", self.close)
        menu.exec_(self.mapToGlobal(position))


app = QtWidgets.QApplication(sys.argv)
pet = DeskPetG13()
pet.show()
# chat_app = ChatApp()
sys.exit(app.exec_())
