import sys 
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout,QHBoxLayout, QGridLayout,QWidget
                            , QLineEdit, QPushButton, QMessageBox, QSpacerItem, QSizePolicy, QMenu ,QWidget , QGraphicsDropShadowEffect)
from PyQt5.QtGui import QIcon,QPixmap , QImage , QColor
from PyQt5.QtCore import Qt , QBuffer, QByteArray
from datetime import datetime,timezone
import numpy as np

import os
from dotenv import load_dotenv
load_dotenv()
class SecondWindow(QMainWindow):
    def __init__(self ,city, main_window ):
        super().__init__()
        self.main_window=main_window
        self.city = city
        self.setWindowTitle("Weather News")
        self.setFixedSize(1366, 705)    
        self.move(0,0)
        self.setWindowIcon(QIcon("images/weatherNews.PNG"))

        ### backgroud image
        self.label_image= QLabel(self)
        self.label_image.setPixmap(QPixmap("images/Sky_Clouds.jpg")) 
        self.label_image.setScaledContents(True)  
        self.label_image.resize(self.size()) 
        
        ### backgroud stage
        self.label_gray = QLabel(self)
        self.label_gray.setStyleSheet("background-color : rgba(0, 0, 0, 80); border-radius:15px;")

        ###Display weather information:
        self.label_degree=QLabel(self)
        self.label_weatherDesc=QLabel(self)
        self.label_location=QLabel(self)
        self.label_icon_second=QLabel(self)
        self.label_today=QLabel(self)
        self.label_icon_loc=QLabel(self)
        
        self.main_layout = QVBoxLayout()
        self.grid_layout = QGridLayout()

        self.initUI()
            

    def initUI(self):

        self.central_weidget=QWidget(self)
        self.setCentralWidget(self.central_weidget)

        ### backgroud stage
        self.label_gray_Width = self.width() * 0.90 
        self.label_gray_height = self.height() * 0.95
        self.label_gray.setGeometry(int((self.width()-self.label_gray_Width)//2),int((self.height()-self.label_gray_height)//2),int(self.label_gray_Width),int(self.label_gray_height))
        
        ###
        box_gray=QHBoxLayout(self.label_gray)
        box_gray.setAlignment(Qt.AlignCenter)
        self.central_weidget.setLayout(box_gray)

        ### less information 
        self.button_moreInfo=QPushButton("less information",self)
        self.button_moreInfo.setFixedSize(180,27)
        self.button_moreInfo.move(1100,25) 
        self.button_moreInfo.setObjectName("moreInfo") 
        self.setStyleSheet("""
            QPushButton#moreInfo {
                color: white;
                font-size: 15px;
                border-radius: 15px;
                background-color: rgba(0, 0, 0, 100);
            }
            QPushButton#moreInfo:hover {
                color: white;
                font-size: 15px;
                border-radius: 15px;
                background-color: rgba(0, 0, 0, 160);  
            }
        """)
        self.button_moreInfo.clicked.connect(self.go_back)
        self.on_click()

        """try:
            print(dir(self))
        except Exception as e:
            print(f"Error: {e}")"""     

    def on_click(self):
        
        while not self.city:  
            QMessageBox.warning(self, "Error", f"Please enter correct city name {self.city}!")
            return  
        API_key = os.getenv("API_KEY")
        url =f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={API_key}"
        reponse = requests.get(url)
        if reponse.status_code != 200:
            QMessageBox.critical(self, "Error", f"Weather data for this city ({self.city}) has not been found!")
            return 

        data = reponse.json()
        self.weather= data["weather"][0]["main"]
        self.degree=data["main"]["temp"] -273.15    
        self.country=data["sys"]["country"]
        self.name=data["name"]
        self.temp_min=data["main"]["temp_max"] -273.15
        self.temp_max=data["main"]["temp_min"] -273.15
        self.clouds=data["clouds"]["all"]
        self.wind=data["wind"]["speed"]
        sunrise_timestamp=data["sys"]["sunrise"]
        sunset_timestamp=data["sys"]["sunset"]
        self.sunrise=datetime.fromtimestamp(sunrise_timestamp,timezone.utc).strftime('%H:%M:%S')
        self.sunset=datetime.fromtimestamp(sunset_timestamp,timezone.utc).strftime('%H:%M:%S')
        self.humidity=data["main"]["humidity"] 
        self.visibil=data["visibility"]
       
        day_today=data["dt"]
        self.today = datetime.fromtimestamp(day_today, timezone.utc).strftime('%a, %b %d, %Y')      
        self.name_day = datetime.fromtimestamp(day_today, timezone.utc).strftime('%a')
        self.name_month = datetime.fromtimestamp(day_today, timezone.utc).strftime('%B')
        self.day_number = datetime.fromtimestamp(day_today, timezone.utc).strftime('%d')
        self.year = datetime.fromtimestamp(day_today, timezone.utc).strftime('%Y')
        self.latitude = data["coord"]["lat"]
        self.longitude = data["coord"]["lon"]
        ### other info:
        url_day=f"http://api.openweathermap.org/data/2.5/forecast?lat={self.latitude}&lon={self.longitude}&appid={API_key}" 
        reponse_day = requests.get(url_day)
        data_days= reponse_day.json()
        counter = 0
        forecasted_data={}
        day_add=set()
        for forecast in data_days["list"]:
            time_full = forecast["dt_txt"]
            date_forecast = datetime.strptime(time_full, "%Y-%m-%d %H:%M:%S").date()
            date_object = datetime.strptime(str(date_forecast), "%Y-%m-%d")
            day_of_week = date_object.strftime("%A")

            if counter <= 5 and day_of_week not in day_add:  
                if counter not in forecasted_data:
                        forecasted_data[counter] = []  
                        temp = forecast["main"]["temp"] -273.15
                        description = forecast["weather"][0]["description"]
                        forecasted_data[counter].append({"day":day_of_week,"temperature": temp, "description": description})
                        day_add.add(day_of_week)
                        counter += 1 
        
        self.day1=forecasted_data[0][0]["day"]
        self.temperature1=forecasted_data[0][0]["temperature"]
        
        self.day2=forecasted_data[1][0]["day"]
        self.temperature2=forecasted_data[1][0]["temperature"]

        self.day3=forecasted_data[2][0]["day"]
        self.temperature3=forecasted_data[2][0]["temperature"]

        self.day4=forecasted_data[3][0]["day"]
        self.temperature4=forecasted_data[3][0]["temperature"]

        self.day5=forecasted_data[4][0]["day"]
        self.temperature5=forecasted_data[4][0]["temperature"]

        self.day6= forecasted_data[5][0]["day"] 
        self.temperature6= forecasted_data[5][0]["temperature"]
        
        self.icon_web=data["weather"][0]["icon"]
        url_icon=f"https://openweathermap.org/img/wn/{self.icon_web}@2x.png"
    
        response = requests.get(url_icon)

        
        if response.status_code == 200:
            
            byte_array = QByteArray(response.content)
            buffer = QBuffer(byte_array)
            buffer.open(QBuffer.ReadOnly)
            self.pixmap = QPixmap()
            if self.pixmap.loadFromData(buffer.readAll()):
                scaled_pixmap = self.pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label_icon_second.setPixmap(scaled_pixmap)
                self.label_icon_second.setScaledContents(True)
                self.label_icon_second.show()  
            else:
                print("Failed to load image into QPixmap")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")

        y_weather = int(self.height() * 0.215)  
        x_weather = int(self.width() * 0.085)
        
        width = int(self.width() * 0.5)
        height = int(self.height() * 0.15)

        self.button_unit = QPushButton("°C / °F",self)

        self.button_unit.setFixedSize(80, 30)
        self.button_unit.move(700,int(y_weather*0.6))
        self.button_unit.setStyleSheet("background-color : #e1f5f2; border-radius:5px; color: black; font-size:20px ;")
       
        self.menu = QMenu(self)
        self.menu.addAction("Celsius (°C)", lambda: self.change_unit("°C"))
        self.menu.addAction("Fahrenheit (°F)", lambda: self.change_unit("°F"))

        self.button_unit.setMenu(self.menu)
        self.current_unit = "°C"
        self.button_unit.show()

        self.label_degree.setGeometry( 750,int(y_weather*0.3),(width),(height*2))
        self.label_degree.setStyleSheet("background-color : transparent ; border-radius:15px;color: white; font-size:70px ; padding: 10px;")
        self.label_degree.setText(f"{self.degree:.0f}{self.current_unit} ")
        
        x_icon = x_weather + width + int(self.width() * 0.02)  
        y_iconSd = int(y_weather*0.1)
        width_icon = int(self.width() * 0.2)  
        height_iconSd = int(height *1.5) 
        self.y_localisation = y_weather + height  
        x_localisation = x_weather  
        width_localisation= width  
        height_localisation = height*0.7

        self.pixmap_icon_loc=QPixmap("images/location_icon.png")
        self.label_icon_loc.setPixmap(self.pixmap_icon_loc)
        self.label_icon_loc.setScaledContents(True)
        self.label_icon_loc.setGeometry(950, int(self.y_localisation*0.55), int(height_iconSd*0.35), int(height_iconSd*0.35))
        self.label_icon_loc.setStyleSheet("background-color: transparent ; padding: 10px;")
        

        self.label_today.setGeometry(int(x_weather * 1.0),int(y_weather*0.2),(width), int(height*0.5)) #transparent
        self.label_today.setStyleSheet("background-color : transparent ; border-radius:15px;color: white; font-size:25px ; padding: 10px;")
        self.label_today.setText(f"{self.name_day }, {self.name_month } {self.day_number},{self.year}")

        self.label_weatherDesc.setGeometry(950,int(y_weather*0.3),width,height)
        self.label_weatherDesc.setStyleSheet("background-color : transparent ; border-radius:15px;color: white; font-size:35px ; padding: 2px;")
        self.label_weatherDesc.setText(f"{self.weather} ")
        self.label_weatherDesc.setAlignment(Qt.AlignLeft | Qt.AlignBottom )

        self.label_icon_second.setGeometry(400, y_iconSd, int(height_iconSd*1.0), int(height_iconSd*1.0))
        self.label_icon_second.setStyleSheet("background-color: transparent ; padding: 10px;")#transparent
 
        
        self.label_location.setGeometry(975, int(self.y_localisation*0.55), int(width_localisation), int(height_localisation))
        self.label_location.setStyleSheet("background-color: transparent; border-radius: 15px; color: white; font-size: 15px; padding: 1px 10px;")
        self.label_location.setAlignment(Qt.AlignLeft | Qt.AlignTop)
       

        self.label_icon_second.setAlignment(Qt.AlignCenter)

        self.label_location.setText(f" {self.name} , {self.country} \n {self.temp_min:.1f}°C-{self.temp_max:.1f}°C")
        self.all_window()
        
    #This function can be changed to a more precise function by introducing conditions on wind and humidity
    def icon(self, temperature):
        
        icon_path = ""
        if temperature < -10:
            icon_path = r"images/severe-weather.png"
        elif -10 <= temperature < 0:
            icon_path = r"images/snow.png"
        elif 0 <= temperature < 5:
            icon_path = r"images/mist.png"
        elif 5 <= temperature < 15:
            icon_path = r"images/47309_overcast_icon.png"
        elif 15 <= temperature < 25:
            icon_path = r"images/rain.png"
        elif 25 <= temperature < 30:
            icon_path = r"images/scattered-thunderstorms.png"
        elif 30 <= temperature < 35:
            icon_path = r"images/hot.png"
        elif 35 <= temperature < 40:
            icon_path = r"images/hot.png"
        else:
            icon_path = r"images/thermometer_1108576.png"
        
        pixmap_icon = QPixmap(icon_path)

        if pixmap_icon.isNull():
            print(f"❌ Failed to load image: {icon_path}")
            return "error.png"  
        else:
            return pixmap_icon

    

    def change_unit(self, unit):
        
        if unit == "°F":
            self.degree = (self.degree * 9/5) + 32
        else:
            self.degree = (self.degree - 32) * 5/9
        self.current_unit = unit
        self.label_degree.setText(f"{self.degree:.0f}{self.current_unit} ")


    def cree_window(self, image, txt, value, x,y , xwin,ywin):

        self.window = QWidget()
        self.window.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-radius: 10px;")
        self.box_layout = QVBoxLayout(self.window)
        self.label_image = QLabel(self)
        self.pixmap1 = QPixmap(image)
        self.label_image.setPixmap(self.pixmap1)
        self.label_image.setStyleSheet("background-color: transparent") 
        self.label_image.setScaledContents(True)
        self.label_image.setFixedSize(60, 60) 

        self.label_text = QLabel(self)
        self.label_text.setText(txt)
        self.label_text.setStyleSheet("color : white ; font-size: 15px;background-color: transparent;")
        

        self.label_value = QLabel(self)
        self.label_value.setText(value)
        self.label_value.setStyleSheet("color : white ; font-size: 15px;background-color: transparent;")

        self.box_layout.addWidget(self.label_image, alignment=Qt.AlignCenter)
        self.box_layout.addWidget(self.label_text, alignment=Qt.AlignCenter)
        self.box_layout.addWidget(self.label_value, alignment=Qt.AlignCenter)  

        self.grid_layout.addWidget(self.window, x, y)
        self.window.setFixedSize(xwin,ywin)

    def cree_window_day(self, image, txt, value, x,y , xwin,ywin):

        self.window1 = QWidget()
        self.window1.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-radius: 10px;")
        self.box_layout1 = QVBoxLayout(self.window1)
        self.label_image1 = QLabel(self)
        self.pixmap1 = QPixmap(image)
        self.label_image1.setPixmap(self.pixmap1) 
        self.label_image1.setScaledContents(True)
        self.label_image1.setFixedSize(60, 60) 

        self.label_text1 = QLabel(self)
        self.label_text1.setText(txt)
        self.label_text1.setStyleSheet("color : white ; font-size: 15px;")
        

        self.label_value1 = QLabel(self)
        self.label_value1.setText(value)
        self.label_value1.setStyleSheet("color : white ; font-size: 15px;")

        self.box_layout1.addWidget(self.label_text1 , alignment=Qt.AlignCenter)
        self.box_layout1.addWidget(self.label_image1, alignment=Qt.AlignCenter)
        self.box_layout1.addWidget(self.label_value1, alignment=Qt.AlignCenter)  

        self.grid_layout.addWidget(self.window1, x, y)
        self.window1.setFixedSize(xwin,ywin)

    def get_iconWeeks(self, code_weather):
        if code_weather == 0:
            return "images/sun.png"  
        elif code_weather in [1, 2, 3]:
            return "images/cloud.png"  
        elif code_weather in [45, 48]:
            return "images/mist.png" 
        elif code_weather in [51, 53, 55]:
            return "images/light_rain.png"  
        elif code_weather in [56, 57]:
            return "images/heavy-rain.png"  
        elif code_weather in [66, 67]:
            return "images/severe-weather.png" 
        elif code_weather == 61:
            return "images/light_rain.png"  
        elif code_weather == 63:
            return "images/snowy.png"  
        elif code_weather == 65:
            return "images/thunder.png"  
        elif code_weather in [80, 81, 82]:
            return "images/scattered-thunderstorms.png"  
        elif code_weather == 95:
            return "images/thunder.png"  
        elif code_weather in [96, 99]:
            return "images/thunder.png"  
        elif code_weather in [71, 73, 75]:
            return "images/snowflake.png"  
        elif code_weather == 77:
            return "images/heavy-rain.png"  
        elif code_weather in [85, 86]:
            return "images/heavy-rain.png"  
        else:
            return "images/error.png"

    def all_window(self):
        
        
        
        self.cree_window( "images/wind_1.png", "WIND", f"{self.wind *3.6 :.2f} Km/h", 0,0 , 125,125)
        self.cree_window( "images/clouds.png", "CLOUDS", f"{self.clouds}%", 0,1 , 125,125)
        self.cree_window( "images/dawn.png", "SUNRIZE", f"{self.sunrise}", 0,2 , 125,125)
        self.cree_window( "images/sunset.png", "SUNSET", f"{self.sunset}", 0,3 , 125,125)
        self.cree_window( "images/humidity.png", "HUMIDITY", f"{self.humidity}%", 0,4 , 125,125)
        self.cree_window( "images/visibility.png", "VISIBILITY", f"{self.visibil * 0.001} Km", 0,5 , 125,125)

        self.cree_window_day( self.icon(self.temperature1), f"{self.day1}", f"{self.temperature1:.2f}°C", 2,0 , 125,125)
        self.cree_window_day( self.icon(self.temperature2), f"{self.day2}", f"{self.temperature2:.2f}°C", 2,1 , 125,125)
        self.cree_window_day( self.icon(self.temperature3), f"{self.day3}", f"{self.temperature3:.2f}°C", 2,2 , 125,125)
        self.cree_window_day( self.icon(self.temperature4), f"{self.day4}", f"{self.temperature4:.2f}°C", 2,3 , 125,125)
        self.cree_window_day( self.icon(self.temperature5), f"{self.day5}", f"{self.temperature5:.2f}°C", 2,4 , 125,125)
        self.cree_window_day( self.icon(self.temperature6), f"{self.day6}", f"{self.temperature6:.2f}°C", 2,5 , 125,125)

        self.main_layout.addLayout(self.grid_layout)
        
        self.label_gray.setLayout(self.main_layout)

        ####
        self.windowd_title = QWidget()
        self.windowd_title.setStyleSheet("background-color: transparent; border-radius: 10px;")
        self.box_layoutd_title = QVBoxLayout( self.windowd_title)

            
        self.label_title = QLabel(self)
        self.label_title.setStyleSheet("color : white; font-size:15px; font-weight :bold;")
        y_weather = int(self.height() * 0.215)  
        x_weather = int(self.width() * 0.085)
        self.label_title_txt = QLabel(self)
        self.label_title_txt.setGeometry(int(x_weather * 1.2),int(y_weather*2.20),400,40) #transparent
        self.label_title_txt.setStyleSheet("background-color : transparent ; border-radius:15px;color: white; font-size:15px ; padding: 10px; font-weight: bold;")
        self.label_title_txt.setText("Weather forecast for coming days ")
        self.shadow_effect( self.label_title_txt  ,8,5,5, QColor(0,0,0,180))


        self.box_layoutd_title.addWidget(self.label_title , alignment=Qt.AlignCenter)


        self.grid_layout .addWidget(self.windowd_title, 1, 0) 
        self.windowd_title.setFixedSize(125,40)

        self.main_layout = QVBoxLayout()
        
        
        self.main_layout.setAlignment(Qt.AlignBottom)
        #self.main_layout.addLayout(self.grid_layout)

        #self.label_gray.setLayout(self.main_layout)

        ###########################

        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&hourly=temperature_2m,weathercode&timezone=auto"
        response = requests.get(url)
        data_day = response.json()

        current_date = datetime.now().strftime("%Y-%m-%d")
        hourly_temps = data_day["hourly"]["temperature_2m"]
        hourly_times = data_day["hourly"]["time"]
        hourly_codes = data_day["hourly"]["weathercode"]
        
        filtered_times = []
        filtered_temps = []
        icon_day=[]
        for i, time in enumerate(hourly_times):
            
            date = time.split("T")[0]
            if date == current_date:
                filtered_times.append(time)
                filtered_temps.append(hourly_temps[i])
                icon_day.append(hourly_codes[i])
        
        if not filtered_times:
            print("There is no data for the current day.")
            sys.exit()

        self.hours = np.array([datetime.strptime(time, "%Y-%m-%dT%H:%M").strftime("%H:%M") for time in filtered_times])
        self.filtered_temps = filtered_temps


        self.new_central_weidget=QWidget(self)

        ### backgroud stage
        self.label_gray_new = QLabel(self)
        self.label_gray_new.setStyleSheet("background-color : transparent; border-radius:15px;")


        self.label_gray_Width = self.width() * 0.90 
        self.label_gray_height = self.height() * 0.3
        
        self.label_gray_new.setGeometry(int((self.width()-self.label_gray_Width)//2),int((self.height() * 0.215)*3.0),int(self.label_gray_Width),int(self.label_gray_height))
         


        self.label_title_txt2 = QLabel(self)
        
        self.label_title.setStyleSheet("color : #fa9623; font-size:15px; font-weight :bold;")
        y_weather = int(self.height() * 0.215)  
        x_weather = int(self.width() * 0.085)
        self.label_title_txt2 = QLabel(self)
        self.label_title_txt2.setGeometry(int(x_weather * 1.2),int(y_weather*3.30),400,40) #transparent
        self.label_title_txt2.setStyleSheet("background-color : transparent ; border-radius:15px;color: white ; font-size:15px ; padding: 10px; font-weight: bold;")
        self.label_title_txt2.setText("Weather forecast by hour ")
        self.shadow_effect( self.label_title_txt2  ,8,5,5,QColor(0,0,0,180))

        box_gr=QHBoxLayout(self.label_gray_new)
        box_gr.addWidget(self.label_gray_new )
        box_gr.setAlignment(Qt.AlignCenter)
        self.new_central_weidget.setLayout(box_gr)


        self.main_layout_hour = QVBoxLayout()


        y_weather = int(self.height() * 0.215)  
        x_weather = int(self.width() * 0.085)
        self.label_title_x = QLabel(self)
        self.label_title_x.setGeometry(int(x_weather * 0.875),int(y_weather*4.0),1135,5) #transparent
        self.label_title_x.setStyleSheet("background-color : #fa9623 ; border-radius:15px;color: white; font-size:15px ; padding: 10px;")
        
        self.grid_layout_hour = QGridLayout()
        self.grid_layout_hour.setContentsMargins(0, 0, 0, 0) 
        self.grid_layout_hour.setSpacing(10)

        self.main_layout_hour = QVBoxLayout()

        self.grid_layout_hour = QGridLayout()
        square_height = 30  
        y_position = int(y_weather * 4.0) - square_height // 2
        for i in range(18):
            self.window_hour = QWidget()
            self.window_hour.setStyleSheet("background-color: transparent; border-radius: 10px;")
            self.window_hour.setGeometry(int(x_weather * 00.5) + (i * 60), y_position, 50, square_height)
            self.box_layout_hour = QVBoxLayout(self.window_hour)
            self.box_layout_hour.setContentsMargins(0, 0, 0, 0)
            self.label_image_hour = QLabel(self)

            self.pixmap1 = QPixmap(f"{self.get_iconWeeks(icon_day[i])}")
            self.label_image_hour.setPixmap(self.pixmap1) 
            self.label_image_hour.setScaledContents(True)
            self.label_image_hour.setFixedSize(20, 20) 

            weather_icon = self.get_iconWeeks(icon_day[i])
  

            self.label_text_hour = QLabel(self)
            self.label_text_hour.setText(f"{self.hours[i]}")
            self.label_text_hour.setStyleSheet("color : white ;background-color:  transparent ; font-size: 17px;")
            
            self.label_s_hour = QLabel(self)
            self.label_s_hour.setText("🔷") #🔴
            self.label_s_hour.setStyleSheet("color : white ; font-size: 15px;")

            self.label_value_hour = QLabel(self)
            self.label_value_hour.setText(f"{self.filtered_temps[i]}°C")

            self.label_value_hour.setStyleSheet("color : white ; font-size: 15px;")

            self.box_layout_hour.addWidget(self.label_text_hour , alignment=Qt.AlignCenter)
            self.box_layout_hour.addWidget(self.label_image_hour, alignment=Qt.AlignCenter)
            self.box_layout_hour.addWidget(self.label_s_hour, alignment=Qt.AlignCenter)
            self.box_layout_hour.addWidget(self.label_value_hour, alignment=Qt.AlignCenter)  

            self.grid_layout_hour.addWidget(self.window_hour, 0, i)
            self.window_hour.setFixedSize(60,90)

            self.window_hide = QWidget()
            self.window_hide.setStyleSheet("background-color: transparent; border-radius: 10px;")
            self.window_hide.setGeometry(int(x_weather * 00.5) + (i * 60), y_position, 50, square_height)
            self.box_layout_hide = QVBoxLayout(self.window_hide)
            self.box_layout_hide.setContentsMargins(0, 0, 0, 0)
            self.label_image_hide = QLabel(self)
            self.pixmap2 = QPixmap("images/wind_1.png")
           
            self.label_image_hide.setFixedSize(40, 40) 

            self.label_text_hide = QLabel(self)
            self.label_text_hide.setStyleSheet("color : white ; font-size: 15px;")
            

            self.label_value_hide = QLabel(self)
     
            self.label_value_hide.setStyleSheet("color : white ; font-size: 15px;")

            self.box_layout_hide.addWidget(self.label_image_hide, alignment=Qt.AlignCenter)
            self.box_layout_hide.addWidget(self.label_text_hide, alignment=Qt.AlignCenter)
            self.box_layout_hide.addWidget(self.label_value_hide, alignment=Qt.AlignCenter)  

            self.grid_layout_hour.addWidget(self.window_hide, 1, i)
            self.window_hide.setFixedSize(16,16)


        self.main_layout_hour = QVBoxLayout()
        
        
        self.main_layout_hour.setAlignment(Qt.AlignBottom)
        self.main_layout_hour.addLayout(self.grid_layout_hour)

        self.label_gray_new.setLayout(self.main_layout_hour)

    def shadow_effect(self,obj,nbr1,nbr2,nbr3,color):
        shadow=QGraphicsDropShadowEffect() 
        shadow.setBlurRadius(nbr1)
        shadow.setXOffset(nbr2)
        shadow.setYOffset(nbr3)
        shadow.setColor(color)
        obj.setGraphicsEffect(shadow)

    def go_back(self):
        
        self.main_window.show_and_enable_input()
        self.main_window.show()  
        self.close()  
    
                                                                   