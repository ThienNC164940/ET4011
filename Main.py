import sys
import numpy as np
#matplotlib.use('QT5Agg')
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QLabel)
from matplotlib.backends.backend_qt5agg import FigureCanvas 
import pandas as pd 
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from tkinter import *
from pandastable import Table, TableModel
import pandas as pd
df = pd.read_csv('/home/bb3/Desktop/da2_data.csv')
df = df.drop("Unnamed: 0",axis = 1)
df_copy = df.copy()
df_copy["Gas"] = df_copy["Gas"].astype(int)
df_copy["Temperature"] = df_copy["Temperature"].astype(int)
df_copy["Humidity"] = df_copy["Humidity"].astype(int)

df1 = pd.read_csv('/home/bb3/Desktop/hnmap.csv')
df_copy1 = df1.copy()


class ShowData(Frame):
    def __init__(self, parent=None):
        df = pd.read_csv("/home/bb3/Desktop/da2_data.csv")
        df = df.drop("Unnamed: 0",axis = 1)
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('600x400+200+100')
        self.main.title('Data')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)
        self.table = pt = Table(f, dataframe=df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()
        return

def goto(linenum):
    global line
    line = linenum

#Give colors

def checkAQI(dataframe):
    for i in range(0,len(dataframe)):
        if(float(dataframe["Gas"][i])<=350):
            dataframe.at[i,'colors'] = 'green'
        if(float(dataframe["Gas"][i]) > 350):
            dataframe.at[i,'colors'] = 'red'
    return dataframe

#Update new 


def webUpdate():
    import folium
    import pandas as pd
    data = pd.read_csv('/home/bb3/Desktop/da2_data.csv',dtype = str)
    data = data.drop("Unnamed: 0",axis = 1)
    data1 = pd.read_csv('/home/bb3/Desktop/hnmap.csv',dtype = str)
    m = folium.Map(location=[21.0278, 105.8342],zoom_start=9)
    for i in range(0,len(data)):
        folium.CircleMarker(location=[data1.iloc[i]['lathn'],data1.iloc[i]['longhn']], radius=9,color=data.iloc[i]['colors'],fill_color=data.iloc[i]['colors']).add_to(m).add_child(folium.Popup(
           "Gas : {} </br>"
           "Temperature : {} </br>" 
           "Humidity : {}".format(data["Gas"][i],data["Temperature"][i],data["Humidity"][i])))
    m.save('/home/bb3/Desktop/hn_map.html')
#Function update data
def Updatedata():
    df = pd.read_csv('/home/bb3/Desktop/da2_data.csv')
    df = df.drop("Unnamed: 0",axis = 1)
    df_copy = df.copy()    
    df_copy.to_csv('/home/bb3/Desktop/da2_data.csv')
    webUpdate()
    df1 = pd.read_csv('/home/bb3/Desktop/hnmap.csv')
    df_copy = checkAQI(df)    
    print("Success")


class Humidity(QDialog):
    def __init__(self):
        super(Humidity, self).__init__()
        self.setFixedSize(1000, 500)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(280, 450, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, -1, 401, 511))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.webView = QWebEngineView(self.gridLayoutWidget)
        self.webView.load(QUrl('file:///home/bb3/Desktop/hn_map.html'))
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
        
        
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(409, -1, 601, 440))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        df = pd.read_csv('/home/bb3/Desktop/da2_data.csv')
        df = df.drop("Unnamed: 0",axis = 1)
        df_copy = df.copy()
        df_copy["Gas"] = df_copy["Gas"].astype(int)
        df_copy["Temperature"] = df_copy["Temperature"].astype(int)
        df_copy["Humidity"] = df_copy["Humidity"].astype(int)
        my_dpi = 96
        fig, ax1 = plt.subplots(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
        ax1.plot(range(len(df_copy)),df_copy['Humidity'],label = 'Humidity index',color = 'orange')
        ax1.set_xlabel('STT')
        ax1.set_ylabel('Humidity (%)')
        ax1.legend(loc="upper right")
        
        
        self.plotWidget = FigureCanvas(fig)
        print(self.gridLayout_2)
        self.gridLayout_2.addWidget(self.plotWidget)
        

        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.accept) #Dialog.accept
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


class Temperature(QDialog):
    def __init__(self):
        super(Temperature, self).__init__()
        self.setFixedSize(1000, 500)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(280, 450, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, -1, 401, 511))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.webView = QWebEngineView(self.gridLayoutWidget)
        self.webView.load(QUrl('file:///home/bb3/Desktop/hn_map.html'))
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
        
        
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(409, -1, 601, 440))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        df = pd.read_csv('/home/bb3/Desktop/da2_data.csv')
        df = df.drop("Unnamed: 0",axis = 1)
        df_copy = df.copy()
        df_copy["Gas"] = df_copy["Gas"].astype(int)
        df_copy["Temperature"] = df_copy["Temperature"].astype(int)
        df_copy["Humidity"] = df_copy["Humidity"].astype(int)
        my_dpi = 96
        fig, ax1 = plt.subplots(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
        ax1.plot(range(len(df_copy)),df_copy['Temperature'],label = 'Temperature index',color = 'orange')
        ax1.set_xlabel('STT')
        ax1.set_ylabel('Temperature (C)')
        ax1.legend(loc="upper right")
        
        
        self.plotWidget = FigureCanvas(fig)
        print(self.gridLayout_2)
        self.gridLayout_2.addWidget(self.plotWidget)
        

        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.accept) #Dialog.accept
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


class Gas(QDialog):
    def __init__(self):
        super(Gas, self).__init__()
        self.setFixedSize(1000, 500)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(280, 450, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, -1, 401, 511))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.webView = QWebEngineView(self.gridLayoutWidget)
        self.webView.load(QUrl('file:///home/bb3/Desktop/hn_map.html'))
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
        
        
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(409, -1, 601, 440))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        df = pd.read_csv('/home/bb3/Desktop/da2_data.csv')
        df = df.drop("Unnamed: 0",axis = 1)
        df_copy = df.copy()
        df_copy["Gas"] = df_copy["Gas"].astype(int)
        df_copy["Temperature"] = df_copy["Temperature"].astype(int)
        df_copy["Humidity"] = df_copy["Humidity"].astype(int)
        my_dpi = 96
        fig, ax1 = plt.subplots(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
        ax1.plot(range(len(df_copy)),df_copy['Gas'],label = 'Gas index',color = 'orange')
        ax1.set_xlabel('STT')
        ax1.set_ylabel('Gas (ppm)')
        ax1.legend(loc="upper right")
        
        
        self.plotWidget = FigureCanvas(fig)
        print(self.gridLayout_2)
        self.gridLayout_2.addWidget(self.plotWidget)
        

        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.accept) #Dialog.accept
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))




#Main window
class Ui_Dialog(QtWidgets.QWidget,QtWidgets.QApplication):
    def __init__(self):
        super(Ui_Dialog,self).__init__()
        self.setFixedSize(400,300)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(120, 20, 160, 191))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 1, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 4, 0, 1, 1)
        
        #set function
        self.pushButton_3.clicked.connect(self.showGas)
        self.pushButton.clicked.connect(self.showTemperature)
        self.pushButton_2.clicked.connect(self.showHumidity)
        self.pushButton_4.clicked.connect(Updatedata)
        self.pushButton_5.clicked.connect(self.Data)

        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.reject)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def showGas(self):
        s_gas = Gas()
        s_gas.exec_()
    def showTemperature(self):
        s_Temperature = Temperature()
        s_Temperature.exec_()
    def showHumidity(self):
        s_Humidity = Humidity()
        s_Humidity.exec_()
    def Data(self):
        test = ShowData()
        test.mainloop()
        print("Data function success")


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Main menu"))
        self.pushButton.setText(_translate("Dialog", "Temperature data"))
        self.pushButton_4.setText(_translate("Dialog", "Update"))
        self.pushButton_2.setText(_translate("Dialog", "Humidity data"))
        self.pushButton_3.setText(_translate("Dialog", "Gas data"))
        self.pushButton_5.setText(_translate("Dialog", "Data"))
    def reject(self):
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())
