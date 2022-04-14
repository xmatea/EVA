# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EfficiencyUIHSFFzK.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_EfficienyCorrection(object):
    def setupUi(self):
        print('in setup')
        if self.objectName():
            self.setObjectName("Efficiency Correction")
        print('1')
        self.resize(1542, 682)
        self.Eff_Det_Tab = QTabWidget()
        self.Eff_Det_Tab.setObjectName("Eff_Det_Tab")
        print('1a')
        self.Eff_Det_Tab.setGeometry(QRect(120, 80, 1111, 481))
        print('2')
        font = QFont()
        font.setPointSize(10)
        self.Eff_Det_Tab.setFont(font)
        self.Eff_Det_Tab.setAutoFillBackground(True)
        self.Eff_Det_Tab.setTabBarAutoHide(False)
        print('done self.eff')
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.checkbox_def_det_1 = QCheckBox(self.tab)
        self.checkbox_def_det_1.setObjectName("checkbox_def_det_1")
        self.checkbox_def_det_1.setGeometry(QRect(10, 30, 301, 51))
        self.checkbox_def_det_1.setChecked(True)
        self.Eff_Det_Tab.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.checkBox_def_det_2 = QCheckBox(self.tab_2)
        self.checkBox_def_det_2.setObjectName("checkBox_def_det_2")
        self.checkBox_def_det_2.setGeometry(QRect(10, 30, 301, 51))
        self.checkBox_def_det_2.setChecked(True)
        self.Eff_Det_Tab.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.checkBox_def_det_3 = QCheckBox(self.tab_3)
        self.checkBox_def_det_3.setObjectName("checkBox_def_det_3")
        self.checkBox_def_det_3.setGeometry(QRect(10, 30, 301, 51))
        self.checkBox_def_det_3.setChecked(True)
        self.Eff_Det_Tab.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")
        self.checkBox_Def_det_4 = QCheckBox(self.tab_4)
        self.checkBox_Def_det_4.setObjectName("checkBox_Def_det_4")
        self.checkBox_Def_det_4.setGeometry(QRect(10, 30, 301, 51))
        self.checkBox_Def_det_4.setChecked(True)
        self.Eff_Det_Tab.addTab(self.tab_4, "")
        print('done setup goinf to translate')

        self.retranslateUi(EfficiencyCorrection)

        self.Eff_Det_Tab.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(self.ui.EfficiencyCorrection)
    # setupUi

    def retranslateUi(self, EfficienyCorrection):
        print('re1')
        EfficienyCorrection.setWindowTitle(QCoreApplication.translate("EfficienyCorrection", "Dialog", None))
        print('re1')

        self.checkbox_def_det_1.setText(QCoreApplication.translate("EfficienyCorrection", "Use Defaults", None))
        print('re1')

        self.Eff_Det_Tab.setTabText(self.Eff_Det_Tab.indexOf(self.tab), QCoreApplication.translate("EfficienyCorrection", "Detector 1", None))
        print('re1')

        self.checkBox_def_det_2.setText(QCoreApplication.translate("EfficienyCorrection", "Use Defaults", None))
        print('re1')

        self.Eff_Det_Tab.setTabText(self.Eff_Det_Tab.indexOf(self.tab_2), QCoreApplication.translate("EfficienyCorrection", "Detector 2", None))
        print('re1')

        self.checkBox_def_det_3.setText(QCoreApplication.translate("EfficienyCorrection", "Use Defaults", None))
        print('re1')

        self.Eff_Det_Tab.setTabText(self.Eff_Det_Tab.indexOf(self.tab_3), QCoreApplication.translate("EfficienyCorrection", "Detector 3", None))
        print('re1')

        self.checkBox_Def_det_4.setText(QCoreApplication.translate("EfficienyCorrection", "Use Defaults", None))
        print('re1')

        self.Eff_Det_Tab.setTabText(self.Eff_Det_Tab.indexOf(self.tab_4), QCoreApplication.translate("EfficienyCorrection", "Detector 4", None))

        print('re1')

    # retranslateUi

