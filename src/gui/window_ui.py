# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QComboBox,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 675)
        MainWindow.setMinimumSize(QSize(900, 675))
        MainWindow.setIconSize(QSize(24, 24))
        MainWindow.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setAutoFillBackground(False)
        self.mainHorizontalLayout = QHBoxLayout(self.centralwidget)
        self.mainHorizontalLayout.setSpacing(2)
        self.mainHorizontalLayout.setObjectName(u"mainHorizontalLayout")
        self.mainHorizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.mainHorizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.leftVerticalLayout = QVBoxLayout()
        self.leftVerticalLayout.setSpacing(0)
        self.leftVerticalLayout.setObjectName(u"leftVerticalLayout")
        self.msgPlainTextEdit = QPlainTextEdit(self.centralwidget)
        self.msgPlainTextEdit.setObjectName(u"msgPlainTextEdit")
        self.msgPlainTextEdit.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.msgPlainTextEdit.sizePolicy().hasHeightForWidth())
        self.msgPlainTextEdit.setSizePolicy(sizePolicy)
        self.msgPlainTextEdit.setMinimumSize(QSize(250, 0))
        self.msgPlainTextEdit.setMaximumSize(QSize(250, 16777215))
        self.msgPlainTextEdit.setAutoFillBackground(False)
        self.msgPlainTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.msgPlainTextEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.msgPlainTextEdit.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.msgPlainTextEdit.setUndoRedoEnabled(False)
        self.msgPlainTextEdit.setReadOnly(True)
        self.msgPlainTextEdit.setBackgroundVisible(False)
        self.msgPlainTextEdit.setCenterOnScroll(False)

        self.leftVerticalLayout.addWidget(self.msgPlainTextEdit)


        self.mainHorizontalLayout.addLayout(self.leftVerticalLayout)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.mainHorizontalLayout.addWidget(self.line_3)

        self.centerVerticalLayout = QVBoxLayout()
        self.centerVerticalLayout.setSpacing(0)
        self.centerVerticalLayout.setObjectName(u"centerVerticalLayout")
        self.centerVerticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.aboveFigure = QWidget(self.centralwidget)
        self.aboveFigure.setObjectName(u"aboveFigure")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.aboveFigure.sizePolicy().hasHeightForWidth())
        self.aboveFigure.setSizePolicy(sizePolicy1)

        self.centerVerticalLayout.addWidget(self.aboveFigure)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.centerVerticalLayout.addWidget(self.line)

        self.belowFigure = QWidget(self.centralwidget)
        self.belowFigure.setObjectName(u"belowFigure")

        self.centerVerticalLayout.addWidget(self.belowFigure)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.centerVerticalLayout.addWidget(self.line_2)

        self.resultLabel = QLabel(self.centralwidget)
        self.resultLabel.setObjectName(u"resultLabel")
        sizePolicy1.setHeightForWidth(self.resultLabel.sizePolicy().hasHeightForWidth())
        self.resultLabel.setSizePolicy(sizePolicy1)
        self.resultLabel.setMaximumSize(QSize(16777215, 50))
        self.resultLabel.setAlignment(Qt.AlignCenter)

        self.centerVerticalLayout.addWidget(self.resultLabel)


        self.mainHorizontalLayout.addLayout(self.centerVerticalLayout)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.mainHorizontalLayout.addWidget(self.line_4)

        self.rightVerticalLayoutWidget = QWidget(self.centralwidget)
        self.rightVerticalLayoutWidget.setObjectName(u"rightVerticalLayoutWidget")
        self.rightVerticalLayout = QVBoxLayout(self.rightVerticalLayoutWidget)
        self.rightVerticalLayout.setSpacing(2)
        self.rightVerticalLayout.setObjectName(u"rightVerticalLayout")
        self.rightVerticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.paramWidget = QWidget(self.rightVerticalLayoutWidget)
        self.paramWidget.setObjectName(u"paramWidget")

        self.rightVerticalLayout.addWidget(self.paramWidget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightVerticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.setParamButton = QPushButton(self.rightVerticalLayoutWidget)
        self.setParamButton.setObjectName(u"setParamButton")

        self.horizontalLayout.addWidget(self.setParamButton)

        self.resetParamButton = QPushButton(self.rightVerticalLayoutWidget)
        self.resetParamButton.setObjectName(u"resetParamButton")

        self.horizontalLayout.addWidget(self.resetParamButton)


        self.rightVerticalLayout.addLayout(self.horizontalLayout)

        self.line_5 = QFrame(self.rightVerticalLayoutWidget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.rightVerticalLayout.addWidget(self.line_5)

        self.stopAlgorithmButton = QPushButton(self.rightVerticalLayoutWidget)
        self.stopAlgorithmButton.setObjectName(u"stopAlgorithmButton")
        self.stopAlgorithmButton.setEnabled(False)

        self.rightVerticalLayout.addWidget(self.stopAlgorithmButton)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(2)
        self.label = QLabel(self.rightVerticalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(40, 16777215))
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.aboveFigureComboBox = QComboBox(self.rightVerticalLayoutWidget)
        self.aboveFigureComboBox.setObjectName(u"aboveFigureComboBox")

        self.gridLayout.addWidget(self.aboveFigureComboBox, 3, 1, 1, 1)

        self.belowFigureComboBox = QComboBox(self.rightVerticalLayoutWidget)
        self.belowFigureComboBox.setObjectName(u"belowFigureComboBox")

        self.gridLayout.addWidget(self.belowFigureComboBox, 4, 1, 1, 1)

        self.algorithmComboBox = QComboBox(self.rightVerticalLayoutWidget)
        self.algorithmComboBox.setObjectName(u"algorithmComboBox")

        self.gridLayout.addWidget(self.algorithmComboBox, 2, 1, 1, 1)

        self.label_4 = QLabel(self.rightVerticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.label_3 = QLabel(self.rightVerticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.clientComboBox = QComboBox(self.rightVerticalLayoutWidget)
        self.clientComboBox.setObjectName(u"clientComboBox")

        self.gridLayout.addWidget(self.clientComboBox, 1, 1, 1, 1)

        self.label_2 = QLabel(self.rightVerticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 3)

        self.rightVerticalLayout.addLayout(self.gridLayout)

        self.backendCheckBox = QCheckBox(self.rightVerticalLayoutWidget)
        self.backendCheckBox.setObjectName(u"backendCheckBox")
        self.backendCheckBox.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.backendCheckBox.sizePolicy().hasHeightForWidth())
        self.backendCheckBox.setSizePolicy(sizePolicy2)
        self.backendCheckBox.setMinimumSize(QSize(250, 0))
        self.backendCheckBox.setMaximumSize(QSize(250, 16777215))
        self.backendCheckBox.setCheckable(True)

        self.rightVerticalLayout.addWidget(self.backendCheckBox)


        self.mainHorizontalLayout.addWidget(self.rightVerticalLayoutWidget)

        self.mainHorizontalLayout.setStretch(0, 1)
        self.mainHorizontalLayout.setStretch(2, 100)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u6eda\u73e0\u8f74\u627f\u6545\u969c\u68c0\u6d4b", None))
        self.resultLabel.setText("")
        self.setParamButton.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u53c2\u6570", None))
        self.resetParamButton.setText(QCoreApplication.translate("MainWindow", u"\u8fd8\u539f\u53c2\u6570", None))
        self.stopAlgorithmButton.setText(QCoreApplication.translate("MainWindow", u"\u6682\u505c\u7b97\u6cd5", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5ba2\u6237\u7aef", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u56fe2", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u56fe1", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u7b97\u6cd5", None))
        self.backendCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u5141\u8bb8\u8be5\u5ba2\u6237\u7aef\u7b97\u6cd5\u540e\u53f0\u8fd0\u884c", None))
    # retranslateUi

