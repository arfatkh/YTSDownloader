#!/usr/bin/python3
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from bs4 import BeautifulSoup
import os
import zipfile
import sys
import concurrent.futures
import configparser
import subprocess






class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setWindowIcon(QtGui.QIcon('icon.png'))
        self.Entry = QtWidgets.QLineEdit(Dialog)
        self.Entry.setGeometry(QtCore.QRect(30, 30, 231, 31))
        self.Entry.setMouseTracking(False)
        #self.Entry.setPlainText("")
        self.Entry.setObjectName("Entry")
        self.list_area = QtWidgets.QScrollArea(Dialog)
        self.list_area.setGeometry(QtCore.QRect(29, 79, 231, 191))
        self.list_area.setWidgetResizable(True)
        self.list_area.setObjectName("list_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 229, 189))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.movie_list = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.movie_list.setGeometry(QtCore.QRect(0, 0, 231, 192))
        self.movie_list.setWordWrap(True)
        self.movie_list.setItemAlignment(QtCore.Qt.AlignLeading)
        self.movie_list.setObjectName("movie_list")
        self.list_area.setWidget(self.scrollAreaWidgetContents)
        self.movie_poster = QtWidgets.QLabel(Dialog)
        self.movie_poster.setAutoFillBackground(True)
        self.movie_poster.setStyleSheet("background-color: white; border: 1.3px inset grey")
        self.movie_poster.setGeometry(QtCore.QRect(270, 80, 101, 121))
        self.movie_poster.setPixmap(QtGui.QPixmap(""))
        self.movie_poster.setScaledContents(True)
        self.movie_poster.setObjectName("movie_poster")
        self.quality_box = QtWidgets.QComboBox(Dialog)
        self.quality_box.setGeometry(QtCore.QRect(270, 220, 86, 25))
        self.quality_box.setEditable(False)
        self.quality_box.setObjectName("quality_box")
        self.quality_box.setEnabled(False)
        self.subtitle = QtWidgets.QCheckBox(Dialog)
        self.subtitle.setGeometry(QtCore.QRect(270, 200, 92, 23))
        self.subtitle.setTristate(False)
        self.subtitle.setEnabled(False)
        self.subtitle.setObjectName("subtitle")
        self.search_btn = QtWidgets.QPushButton(Dialog)
        self.search_btn.setGeometry(QtCore.QRect(270, 30, 81, 31))
        self.search_btn.setObjectName("search_btn")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(270, 250, 51, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Start")
        self.pushButton.setEnabled(False)
        self.toolButton = QtWidgets.QToolButton(Dialog)
        self.toolButton.setGeometry(QtCore.QRect(325, 250, 31, 31))
        self.toolButton.setObjectName("toolButton")


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Movie Downloader"))
        self.subtitle.setText(_translate("Dialog", "Subtitle"))
        self.search_btn.setText(_translate("Dialog", "Search"))
        self.toolButton.setText(_translate("Dialog", "..."))


    # SETTING  DIALOG BOX

    def settingsetupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(400, 300)
       
        Dialog.setAutoFillBackground(False)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(110, 260, 281, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 401, 261))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.checkBox = QtWidgets.QCheckBox(self.tab)
        self.checkBox.setGeometry(QtCore.QRect(10, 10, 191, 23))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 32, 161, 23))
        self.checkBox_2.setObjectName("checkBox_2")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.settingretranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def settingretranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.checkBox.setText(_translate("Dialog", "Auto Download Torrent"))
        self.checkBox_2.setText(_translate("Dialog", "Download Subtitles"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Downloads"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Test"))

class Movie:

    def __init__(self,name,qualities,subtitle_link,poster):

        self.name=name
        self.qualities=qualities
        self.subtitle_link=subtitle_link
        self.poster=poster

    def download_subtitle(self):

        responce=requests.get(self.subtitle_link)
        soup=BeautifulSoup(responce.content,'html.parser')
        lang=soup.find("span",class_="sub-lang",text="English")
        l=lang.findNext("a")['href']
        
        print(f"Printing L ",l)

        responce2=requests.get(l)
        soup2=BeautifulSoup(responce2.content,'html.parser')
        d_link=soup2.find("a",class_="btn-icon download-subtitle")["href"]
        d_link="https://www.yifysubtitles.org"+ d_link

        srt=requests.get(d_link)


        with open(self.name+".zip",'wb') as s:
            s.write(srt.content)
            with zipfile.ZipFile(self.name+".zip") as zf:
                zf.extractall()
        os.remove(self.name+".zip")



    def download(self,quality_index):

        
        file_=requests.get(self.qualities[quality_index][1])      

        if ui.subtitle.isChecked():
            self.download_subtitle()            

        with open(f'{self.name}.torrent','wb') as f:
            f.write(file_.content)

        if configuration.getboolean('Downloads','auto_start_torrent'):
            subprocess.Popen(['xdg-open', self.name+'.torrent'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       

def get_defaults():

    parser=configparser.ConfigParser()

    if os.path.exists('config.ini'):
       parser.read('config.ini')
       return parser


    else:

        parser['Downloads']={
            "auto_start_torrent":True,
            "download_subs":True
        }

        with open('config.ini','w') as f:
            parser.write(f)
        return parser


def display_settings():
    SettingDialog.show()

    parse_obj=get_defaults()

    auto_start_torrent=parse_obj.getboolean('Downloads','auto_start_torrent')
    auto_subs=parse_obj.getboolean('Downloads','download_subs')

    setting.checkBox.setChecked(auto_start_torrent)
    setting.checkBox_2.setChecked(auto_subs)
    
def change_settings():
    SettingDialog.hide()
    auto_start_torrent=setting.checkBox.isChecked()
    download_subs=setting.checkBox_2.isChecked()

    parser=configparser.ConfigParser()
    parser['Downloads']={
        'auto_start_torrent':auto_start_torrent,
        'download_subs':download_subs
    }
    with open('config.ini','w') as f:
        parser.write(f)



if __name__ == "__main__":

    configuration=get_defaults()
    
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    SettingDialog = QtWidgets.QDialog()

    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    setting=Ui_Dialog()
    setting.settingsetupUi(SettingDialog)

    def update_info(index):
        ui.quality_box.clear()
        q=QtGui.QPixmap()
        q.loadFromData(available_movies[index].poster,"JPG")
        ui.movie_poster.setPixmap(q)
        
        for q in available_movies[index].qualities:
            ui.quality_box.addItem(q[0])

    
    
            
         
    def get_search(movie_name):



        ui.Entry.clear()
        ui.movie_list.clear()


        global available_movies
        available_movies=[]


       
    
        response = requests.get("https://yts.mx/browse-movies/"+movie_name)    
    
    

        soup = BeautifulSoup(response.content,"html.parser")
        search_result =soup.find_all("div",class_="browse-movie-bottom")
    
        
         
        ui.movie_list.setFocus()
        
        def test(movie):

            name = movie.find("a").get_text()
            movie_page=requests.get(movie.find("a")["href"])

            
            

            soup2=BeautifulSoup(movie_page.content,"html.parser")
            qualities=soup2.find_all("div",class_="modal-torrent")
            subtitle_link=soup2.find("a",text="Subtitles")["href"]
            movieposter=requests.get(soup2.find("img",class_="img-responsive")['src']).content
            
            

            qualities_=[]

            for div in qualities:
                
                quality_name=f'{div.find("span").get_text()}({div.find("p",class_="quality-size").get_text()}) | {div.find_all("p",class_="quality-size")[1].get_text()}'
                download_link=div.find("a",class_="download-torrent button-green-download2-big")["href"]
                download_link_torrent=div.find("a",class_="magnet-download download-torrent magnet")["href"]
                qualities_.append((quality_name,download_link,download_link_torrent))


            available_movies.append(Movie(name,qualities_,subtitle_link,movieposter))


        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(test,search_result)
    
    
        for i,n in enumerate(available_movies,start=1):
            ui.movie_list.addItem(f'{i} :{n.name}')
        
        ui.movie_list.setCurrentRow(0)


     

       

            
        
    
   


    ui.search_btn.clicked.connect(lambda :  get_search(ui.Entry.text()))
    ui.movie_list.itemSelectionChanged.connect(lambda:update_info(ui.movie_list.currentRow()))
    ui.movie_list.itemSelectionChanged.connect(lambda:ui.pushButton.setEnabled(True))
    ui.movie_list.itemSelectionChanged.connect(lambda:ui.quality_box.setEnabled(True))
    ui.movie_list.itemSelectionChanged.connect(lambda:ui.subtitle.setEnabled(True))
    if configuration.getboolean('Downloads','download_subs'):
        ui.subtitle.setChecked(True)



   
    ui.pushButton.clicked.connect(lambda : available_movies[ui.movie_list.currentRow()].download(ui.quality_box.currentIndex()))
    ui.toolButton.clicked.connect(lambda : display_settings())
    setting.buttonBox.accepted.connect(lambda : change_settings())
    
    
    
    Dialog.show()
    
    sys.exit(app.exec_())

