import sys 
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout,QHBoxLayout, QGridLayout,QWidget
                            , QLineEdit, QPushButton, QMessageBox, QSpacerItem, QSizePolicy, QMenu ,QWidget , QListWidget)
from PyQt5.QtGui import QIcon,QPixmap , QImage
from PyQt5.QtCore import Qt , QBuffer, QByteArray
from PyQt5.QtCore import Qt 
from datetime import datetime,timezone
from weather import SecondWindow

import os
from dotenv import load_dotenv
load_dotenv()
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather News")
        
        self.move(500,100)
        self.setFixedSize(400,500)
        self.setWindowIcon(QIcon("images/weatherNews.PNG"))
        
        ### backgroud image
        self.label_image= QLabel(self)
        self.label_image.setPixmap(QPixmap("images/Sky_Clouds.jpg")) 
        self.label_image.setScaledContents(True)  
        self.label_image.resize(self.size())  

        
        ### backgroud stage
        self.label_gray = QLabel(self)
        self.label_gray.setStyleSheet("background-color : rgba(0, 0, 0, 140); border-radius:15px;")

        ### Enter the city
        self.citySearchedList=QListWidget(self)
        self.line_edits=QLineEdit(self)
        self.line_edits.setEnabled(True)
        
        ###Display weather information:
        self.label_weather=QLabel(self)
        self.label_location=QLabel(self)
        self.label_localisation=QLabel(self)
        self.label_icon=QLabel(self)
        self.label_image_hide=QLabel(self) 

        self.initUI()


    def initUI(self):
        self.central_weidget=QWidget(self)
        self.setCentralWidget(self.central_weidget)

        ### backgroud stage
        self.label_gray_Width = self.width() * 0.90 
        self.label_gray_height = self.height() * 0.95
        self.label_gray.setGeometry(int((self.width()-self.label_gray_Width)//2),int((self.height()-self.label_gray_height)//2),int(self.label_gray_Width),int(self.label_gray_height))
        
        ###
        self.button=QPushButton("search",self)
        box_gray=QHBoxLayout(self.label_gray)
        box_gray.setAlignment(Qt.AlignCenter)
        self.central_weidget.setLayout(box_gray)

        ### Enter the city 
        self.line_edits.setGeometry(int(self.label_gray.width() *0.15),55,int(self.width()*(1/2)+5),35)
        self.button.setGeometry(int(self.label_gray.width() *0.8),55,int(self.width()*(1/6)),35)
        self.line_edits.setStyleSheet("background-color : #e0f3fa ;"
                                    " border-radius:15px;"
                                    "font-size : 15px;"
                                    )
        self.line_edits.setPlaceholderText("Weather in your city...")
        self.line_edits.setEnabled(True)
        self.button.setObjectName("button") 
        self.setStyleSheet("""
            QPushButton {
                font-size: 15px;
                border-radius: 15px;
                background-color: hsl(196, 92%, 38%);
            }
            QPushButton:hover {
                font-size: 15px;
                border-radius: 15px;
                background-color: hsl(196, 92%, 60%);  
            }
        """)
        self.button.setEnabled(True)
        #####################"search city"################
        
        self.citySearchedList.setGeometry(int(self.label_gray.width() *0.15),80,int(self.width()*(1/2)),150)
        self.citySearchedList.setStyleSheet("""
                                            border-radius: 10px;
                                            font-size: 15px;
                                            font-family: Arial;
                                            background: #e0f3fa;
                                            color: black;
                                            padding-left: 10px;
                                            padding-top: 20px;
                                        """)
        self.citySearchedList.hide()
        self.line_edits.textChanged.connect(self.searchbar)
        self.citySearchedList.itemClicked.connect(self.selectItem)
        self.citySearchedList.raise_()
        self.Api_Key = os.getenv("API_KEY")
        self.base_url_CityEntered = "http://api.openweathermap.org/geo/1.0/direct?appid=" + self.Api_Key


        ##################################################
        
        x_icon_x =  int(self.width() * 0.085) + int(self.height() * 0.1) 
        self.pixmap_image_hide=QPixmap("images/icron_weatherr.png")
        self.label_image_hide.setPixmap(self.pixmap_image_hide)
        self.label_image_hide.setScaledContents(True)
        self.label_image_hide.setGeometry(x_icon_x, int(int(self.height() * 0.215)*0.7), int(self.width() * 0.6) , int(self.height() * 0.175 *2.5))
        self.label_image_hide.setStyleSheet("background-color: transparent ; padding: 10px;")
        self.label_image_hide.setAlignment(Qt.AlignCenter)
     
        self.changed_label()

        self.button.clicked.connect(self.on_click)


    def searchbar(self):
        query = self.line_edits.text().strip()
        if not query:
            self.citySearchedList.hide()
            return
        
        params = {"q": query, "limit": 5, "appid": self.Api_Key}
        response = requests.get(self.base_url_CityEntered, params=params)

        if response.status_code == 200:
            cities = response.json()
            self.citySearchedList.clear()  
            if not cities:
                self.citySearchedList.hide()
                return

            for city in cities:
                city_name = city.get('name', 'Unknown')
                country = city.get('country', 'Unknown')
                self.citySearchedList.addItem(f"◉ {city_name}, {country}")

            self.citySearchedList.show()  
        else:
            print("Server connection error:", response.status_code)

    def selectItem(self, item) :
        self.line_edits.setText(item.text()[2:])  
        self.citySearchedList.hide()
        self.citySearchedList.clear()
    
    def changed_label(self):
        self.main_layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        
        ### wind 
        self.window1 = QWidget()
        self.window1.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-radius: 10px;")
        self.box_layout1 = QVBoxLayout(self.window1)
        self.label_image1 = QLabel(self)
        self.pixmap1 = QPixmap("images/wind_1.png")
        self.label_image1.setPixmap(self.pixmap1) 
        self.label_image1.setStyleSheet("background-color: transparent")
        self.label_image1.setScaledContents(True)
        self.label_image1.setFixedSize(60, 60) 

        self.label_text1 = QLabel(self)
        self.label_text1.setText(f"WIND")
        self.label_text1.setStyleSheet("color : white; background-color: transparent;")
        

        self.label_value1 = QLabel(self)
        self.label_value1.setStyleSheet("color : white;background-color: transparent;")

        self.box_layout1.addWidget(self.label_image1, alignment=Qt.AlignCenter)
        self.box_layout1.addWidget(self.label_text1, alignment=Qt.AlignCenter)
        self.box_layout1.addWidget(self.label_value1, alignment=Qt.AlignCenter)  

        self.grid_layout.addWidget(self.window1, 0, 0)
        self.window1.setFixedSize(110,110)

        ### clouds
        self.window2 = QWidget()
        self.window2.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-radius: 10px;")
        self.box_layout2 = QVBoxLayout(self.window2)
        
        self.label_image2 = QLabel(self)
        self.pixmap2 = QPixmap("images/clouds.png") 
        self.label_image2.setPixmap(self.pixmap2)
        self.label_image2.setStyleSheet("background-color: transparent")
        self.label_image2.setScaledContents(True)
        self.label_image2.setFixedSize(60, 60)

        self.label_text2 = QLabel(self)
        self.label_text2.setText(f"CLOUDS")
        self.label_text2.setStyleSheet("color : white;background-color: transparent;")
        
        self.label_value2= QLabel(self)
        self.label_value2.setStyleSheet("color : white;background-color: transparent;") 

        self.box_layout2.addWidget(self.label_image2, alignment=Qt.AlignCenter)
        self.box_layout2.addWidget(self.label_text2, alignment=Qt.AlignCenter)
        self.box_layout2.addWidget(self.label_value2, alignment=Qt.AlignCenter)  

        self.grid_layout.addWidget(self.window2, 0, 1)
        self.window2.setFixedSize(110,110)

        ### sunrise
        self.window3 = QWidget()
        self.window3.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-radius: 10px;")
        self.box_layout3 = QVBoxLayout(self.window3)

        self.label_image3 = QLabel(self)
        self.pixmap3 = QPixmap("images/dawn.png")  
        self.label_image3.setPixmap(self.pixmap3)
        self.label_image3.setStyleSheet("background-color: transparent")
        self.label_image3.setScaledContents(True)
        self.label_image3.setFixedSize(60, 60)
            
        self.label_text3 = QLabel(self)
        self.label_text3.setText(f"SUNRIZE")
        self.label_text3.setStyleSheet("color : white;background-color: transparent;")

        
        self.label_value3 = QLabel(self)
        self.label_value3.setStyleSheet("color : white;background-color: transparent;") 

        
        self.box_layout3.addWidget(self.label_image3, alignment=Qt.AlignCenter)
        self.box_layout3.addWidget(self.label_text3, alignment=Qt.AlignCenter)
        self.box_layout3.addWidget(self.label_value3, alignment=Qt.AlignCenter)  

        self.grid_layout.addWidget(self.window3, 1, 0) 
        self.window3.setFixedSize(110,110)

        ### sunset
        self.window4 = QWidget()
        self.window4.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-radius: 10px;")
        self.box_layout4 = QVBoxLayout(self.window4)

        self.label_image4 = QLabel(self)
        self.pixmap4 = QPixmap("images/sunset.png") 
        self.label_image4.setPixmap(self.pixmap4)
        self.label_image4.setStyleSheet("background-color: transparent")
        self.label_image4.setScaledContents(True)
        self.label_image4.setFixedSize(60, 60)
            
        self.label_text4 = QLabel(self)
        self.label_text4.setText(f"SUNSET")
        self.label_text4.setStyleSheet("color : white;background-color: transparent;")
        
        self.label_value4 = QLabel(self) 
        self.label_value4.setStyleSheet("color : white;background-color: transparent;")

        
        self.box_layout4.addWidget(self.label_image4, alignment=Qt.AlignCenter)
        self.box_layout4.addWidget(self.label_text4, alignment=Qt.AlignCenter)
        self.box_layout4.addWidget(self.label_value4, alignment=Qt.AlignCenter)  

        self.grid_layout.addWidget(self.window4, 1, 1) 
        self.window4.setFixedSize(110,110)

       

        self.main_layout = QVBoxLayout()
        
        spacer = QSpacerItem(20, int(self.height() * 0.215)+int(self.height() * 0.15) , QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)



        self.main_layout.addLayout(self.grid_layout)

        self.label_gray.setLayout(self.main_layout)

    def on_click(self):
        
        self.move(500,100)
        self.setFixedSize(400,500)
        self.label_image_hide.setVisible(False)
        self.citySearchedList.hide()
        #self.changed_window()
        self.label_image.resize(self.size()) 
        self.label_gray_Width = self.width() * 0.90 
        self.label_gray_height = self.height() * 0.95
        self.label_gray.setGeometry(int((self.width()-self.label_gray_Width)//2),int((self.height()-self.label_gray_height)//2),int(self.label_gray_Width),int(self.label_gray_height))
        self.line_edits.setGeometry(int(self.label_gray.width()*0.15),55,int(self.width()*(1/2)),35)
        self.line_edits.setEnabled(True)
        self.button.setGeometry(int(self.label_gray.width() *0.8),55,int(self.width()*(1/6)),35)
        self.button.setEnabled(True)
        
        self.city_name = self.line_edits.text()
        self.line_edits.setEnabled(True)
        #city_name = "london"

        while not self.city_name:  
            QMessageBox.warning(self, "Error", f"Please enter correct city name {self.city_name}!")
            self.line_edits.setFocus() 
            return  
        API_key = os.getenv("API_KEY")
        url =f"https://api.openweathermap.org/data/2.5/weather?q={self.city_name}&appid={API_key}"
        reponse = requests.get(url)
        if reponse.status_code != 200:
            
            QMessageBox.critical(self, "Error", f"Weather data for this city ({self.city_name}) has not been found!")
            self.line_edits.setFocus() 
            return  
        data = reponse.json()
        self.weather= data["weather"][0]["main"]
        self.degree=data["main"]["temp"] -273.15    
        

        self.icon_web=data["weather"][0]["icon"]
        url_icon=f"https://openweathermap.org/img/wn/{self.icon_web}@2x.png"
       
        response = requests.get(url_icon)

        
        if response.status_code == 200:
            
            byte_array = QByteArray(response.content)
            buffer = QBuffer(byte_array)
            buffer.open(QBuffer.ReadOnly)
            self.pixmap = QPixmap()
            if self.pixmap.loadFromData(buffer.readAll()):
                scaled_pixmap = self.pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label_icon.setPixmap(scaled_pixmap)
                self.label_icon.setScaledContents(True)
                self.label_icon.show()  
            else:
                print("Failed to load image into QPixmap")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")

        y_weather = int(self.height() * 0.15)  
        x_weather = int(self.width() * 0.085)
        
        width = int(self.width() * 0.55)
        height = int(self.height() * 0.3)
        
        self.button_unit = QPushButton("°C / °F",self)
        self.button_unit.setFixedSize(60, 25)
        self.button_unit.move(int(x_weather*4),int(y_weather*1.5))
        self.button_unit.setStyleSheet("background-color : #e1f5f2; border-radius:5px; color: black; font-size:15px ;")
        self.menu = QMenu(self)
        self.menu.addAction("Celsius (°C)", lambda: self.change_unit("°C"))
        self.menu.addAction("Fahrenheit (°F)", lambda: self.change_unit("°F"))

        self.button_unit.setMenu(self.menu)
        self.current_unit = "°C"
        self.button_unit.show()

        self.label_weather.setGeometry(int(x_weather),int(y_weather),width,height)#transparent
        self.label_weather.setStyleSheet("background-color : transparent; border-radius:15px;color: white; font-size:25px ; padding: 10px;")
        self.label_weather.setText(f"{self.degree:.1f}{self.current_unit} \n{self.weather}")
        

        x_icon =  x_weather + y_weather + int(self.width() * 0.215)  
        y_icon = int(y_weather*1)
        width_icon = int(self.width() * 0.3)  
        height_icon = int(self.height() * 0.15) *2 

        self.label_icon.setGeometry(x_icon, y_icon, height_icon, height_icon)
        self.label_icon.setStyleSheet("background-color: transparent ; padding: 10px;")#transparent
        self.label_icon.setAlignment(Qt.AlignCenter)
        
        ###localisation  et temperature :
    
        self.country=data["sys"]["country"]
        self.name=data["name"]
        self.temp_min=data["main"]["temp_max"] -273.15
        self.temp_max=data["main"]["temp_min"] -273.15
        self.y_localisation = y_weather + int(height*0.75) 
        x_localisation = x_weather  
        width_localisation= width  
        height_localisation = height*1.0  
        
        self.label_location.setGeometry(int(x_localisation), int(self.y_localisation), int(width_localisation), int(height_localisation))
        self.label_location.setStyleSheet("background-color: transparent; border-radius: 15px; color: white; font-size: 15px; padding: 1px 10px;")
        self.label_location.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label_location.setText(f" {self.name} , {self.country} \n {self.temp_min:.1f}°C-{self.temp_max:.1f}°C")
        
        self.clouds=data["clouds"]["all"]
        self.wind=data["wind"]["speed"]
        sunrise_timestamp=data["sys"]["sunrise"]
        sunset_timestamp=data["sys"]["sunset"]
        self.sunrise=datetime.fromtimestamp(sunrise_timestamp,timezone.utc).strftime('%H:%M:%S')
        self.sunset=datetime.fromtimestamp(sunset_timestamp,timezone.utc).strftime('%H:%M:%S')
        self.humidity=data["main"]["humidity"] 
        self.visibil=data["visibility"]

        
        self.label_value1.setText(f"{self.wind*3.6 :.2f} Km/h") 
        self.label_value2.setText(f"{self.clouds}%")
        self.label_value3.setText(f"{self.sunrise}")
        self.label_value4.setText(f"{self.sunset}")

        
        
        ### more information 
        self.button_moreInfo=QPushButton("more information",self)
        
        self.button_moreInfo.setFixedSize(140,27)
        self.button_moreInfo.move(int(self.label_gray.width() *0.60),int(self.label_gray.height() *(4/95))) 
        self.button_moreInfo.setObjectName("morebutton") 
        
        self.setStyleSheet("""
            QPushButton#morebutton {
                color: white;
                font-size: 15px;
                border-radius: 15px;
                background-color: rgba(0, 0, 0, 100);
            }
            QPushButton#morebutton:hover {
                color: white;
                font-size: 15px;
                border-radius: 15px;
                background-color: rgba(0, 0, 0, 160);  
            }
        """)
        self.button_moreInfo.show()
        #self.button.setEnabled(True)
        self.line_edits.setEnabled(True)
        
        
        
        self.citySearchedList.raise_()
        self.button_moreInfo.clicked.connect(self.open_second_window)
        self.line_edits.setFocus()
        
    def open_second_window(self):
        city = self.city_name
        self.weather = SecondWindow(city, self)
        self.weather.show()
        self.hide()

    def show_and_enable_input(self):
        self.show()  
        self.line_edits.setEnabled(True) 
        self.line_edits.setFocus()
        self.button.setObjectName("button")  
        self.setStyleSheet("""
            QPushButton#button {
                font-size: 15px;
                border-radius: 15px;
                background-color: hsl(196, 92%, 38%);
            }
            QPushButton#button:hover {
                font-size: 15px;
                border-radius: 15px;
                background-color: hsl(196, 92%, 60%);  
            }
        """)

        
    def change_unit(self, unit):
        
        if unit == "°F":
            self.degree = (self.degree * 9/5) + 32
        else:
            self.degree = (self.degree - 32) * 5/9
        self.current_unit = unit
        self.label_weather.setText(f"{self.degree:.1f}{self.current_unit} \n{self.weather}")


    def changed_window(self):
        self.label_image.resize(self.size()) 
        self.label_gray_Width = self.width() * 0.90 
        self.label_gray_height = self.height() * 0.95
        self.label_gray.setGeometry(int((self.width()-self.label_gray_Width)//2),int((self.height()-self.label_gray_height)//2),int(self.label_gray_Width),int(self.label_gray_height))
        self.line_edits.setGeometry(int(self.label_gray.width()*0.15),55,int(self.width()*(1/2)),35)
        self.line_edits.setEnabled(True)
        self.button.setGeometry(int(self.label_gray.width() *0.8),55,int(self.width()*(1/6)),35)
        self.button.setEnabled(True)
    
                                                                         
def main():
    app = QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())

main()