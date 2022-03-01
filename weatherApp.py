# -*- coding: utf-8 -*-
# =============================================================================
# Created on Thu May 24 11:30:36 2018
# @author: Euphemia
# =============================================================================

import sys
if "tkinter" not in sys.modules:
    from tkinter import *
    from tkinter import ttk, messagebox
    from tkinter import messagebox
import weather, iso3166, folium, datetime, time, os, webbrowser

class weatherApp:
    
    def __init__(self, master):
        self.master = master
        self._createGUI()
        self.master.protocol("WM_DELETE_WINDOW", self._safe_close)
        self._chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        self._map_path = 'C:/Users/euphe/OneDrive/Documents/Study/Computer Languages/Python/Projects/Weather/' # where your map will be saved.
        
    def _createGUI(self):
        self.master.title('Euphemia Weather Application')
        self.master.resizable(False, False)
        
        # Frames
        self.frame_header = ttk.Frame(self.master)
        self.frame_content = ttk.Frame(self.master)
        self.frame_submit = ttk.Frame(self.master)
        
        self.frame_header.pack()
        self.frame_content.pack(pady=20)
        self.frame_submit.pack(pady=20)
        
        # Header
        self.logo = PhotoImage(file = 'ews.gif')
        self.label_logo = ttk.Label(self.frame_header, image = self.logo).grid(row = 0, column = 0, rowspan = 2)
        
        # NoteBook
        self.notebook = ttk.Notebook(self.frame_content)
        self.notebook.pack()
        self.frame_ctycntry = ttk.Frame(self.notebook)
        self.frame_ctyid = ttk.Frame(self.notebook)
        self.frame_lonlat = ttk.Frame(self.notebook)
        
        self.notebook.add(self.frame_ctycntry, text ="City/Country")
        self.notebook.add(self.frame_ctyid, text ="City ID")
        self.notebook.add(self.frame_lonlat, text ="Longitude/Latitude")
    
        # City/Country Tab
        self.label_ctynm = ttk.Label(self.frame_ctycntry, text = "City Name")
        self.label_cntrycd = ttk.Label(self.frame_ctycntry, text = "Country Code")
        self.entry_ctynm = ttk.Entry(self.frame_ctycntry, width = 28)
        self.cntrycode = StringVar()
        self.ccvalue = sorted(list(iso3166.countries_by_alpha2.keys()))
        self.combobox_cntrycd = ttk.Combobox(self.frame_ctycntry, textvariable=self.cntrycode, values=self.ccvalue, width = 25)
                
        self.label_ctynm.grid(row=0, column=0, padx =10 , pady = 5)
        self.label_cntrycd.grid(row=1, column=0, padx = 10, pady = 5)
        self.entry_ctynm.grid(row=0, column=1, padx =10 , pady = 5)
        self.combobox_cntrycd.grid(row=1, column=1, padx = 10, pady = 5)
         
        # CityID Tab
        self.label_ctyid = ttk.Label(self.frame_ctyid, text = "City ID")
        self.entry_ctyid = ttk.Entry(self.frame_ctyid, width = 28)
        
        self.label_ctyid.grid(row=0, column=0, padx =30 , pady = 5)
        self.entry_ctyid.grid(row=0, column=1, padx =10 , pady = 5)
        
        # Longitude/Latitude Tab
        self.label_lon = ttk.Label(self.frame_lonlat, text = "Longitude")
        self.label_lat = ttk.Label(self.frame_lonlat, text = "Latitude")
        self.entry_lon = ttk.Entry(self.frame_lonlat, width = 28)
        self.entry_lat = ttk.Entry(self.frame_lonlat, width = 28)
        
        self.label_lon.grid(row=0, column=0, padx = 20 , pady = 5)
        self.label_lat.grid(row=1, column=0, padx = 20, pady = 5)
        self.entry_lon.grid(row=0, column=1, padx = 10 , pady = 5)
        self.entry_lat.grid(row=1, column=1, padx = 10, pady = 5)
        
        self.submit_button = ttk.Button(self.frame_submit, text = 'Submit', command=self._submit_callback)
        self.submit_button.grid(row = 3, column = 1, columnspan = 2)
    
    def _pop_up_window(self, weathercheck):
        
        self.info = {'HEADER': f"{weathercheck.getInfo('name')}'s Current Weather Details"
                    ,'CITY_ID': weathercheck.getInfo('id')
                    ,'CITY_NAME': weathercheck.getInfo('name')
                    ,'COUNTRY_NAME': iso3166.countries_by_alpha2[weathercheck.getInfo('sys','country')].name
                    ,'LONGITUDE': weathercheck.getInfo('coord','lon')
                    ,'LATITUDE': weathercheck.getInfo('coord','lat')
                    ,'DESCRIPTION': weathercheck.getInfo('weather',0,'description')
                    ,'TEMPERATURE': weather.KtoC(weathercheck.getInfo('main','temp'))
                    ,'MIN_TEMPERATURE': weather.KtoC(weathercheck.getInfo('main','temp_min'))
                    ,'MAX_TEMPERATURE': weather.KtoC(weathercheck.getInfo('main','temp_max'))
                    ,'VISIBILITY': weathercheck.getInfo('visibility')
                    ,'PRESSURE': weathercheck.getInfo('pressure')
                    ,'HUMIDITY': weathercheck.getInfo('humidity')
                    ,'WIND_SPEED': weathercheck.getInfo('wind','speed')
                    ,'TDC': weather.dtF(weathercheck.getInfo('dt'))
                    ,'SUNRISE': weather.dtF(weathercheck.getInfo('sys','sunrise'))
                    ,'SUNSET': weather.dtF(weathercheck.getInfo('sys','sunset'))
                }
    
        self.window = Toplevel(self.master)
        self.window.geometry('500x500+50+100')
        
        self.frame_details_header = ttk.Frame(self.window)
        self.frame_details_content= ttk.Frame(self.window)
        
        self.frame_details_header.pack()
        self.frame_details_content.pack()
        
        self.label_l_header = ttk.Label(self.frame_details_header, text = self.info['HEADER'] , font = ('Ariel',10,'bold','underline')).grid(row=0, column=0)
        
        ttk.Label(self.frame_details_content, text = 'City ID : ').grid(row=1, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = self.info['CITY_ID']).grid(row=1, column=1, sticky = 'ne')
        ttk.Label(self.frame_details_content, text = 'City Name : ').grid(row=2, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = self.info['CITY_NAME']).grid(row=2, column=1, sticky = 'ne')
        ttk.Label(self.frame_details_content, text = 'Country Name : ').grid(row=3, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = self.info['COUNTRY_NAME']).grid(row=3, column=1, sticky = 'ne')
        ttk.Label(self.frame_details_content, text = 'Longitude : ').grid(row=4, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = self.info['LONGITUDE']).grid(row=4, column=1, sticky = 'ne')
        ttk.Label(self.frame_details_content, text = 'Latitude : ').grid(row=5, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = self.info['LATITUDE']).grid(row=5, column=1, sticky = 'ne')
        
        ttk.Label(self.frame_details_content, text = 'Description : ').grid(row=6, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = self.info['DESCRIPTION']).grid(row=6, column=1, sticky = 'ne')
        ttk.Label(self.frame_details_content, text = 'Temperature : ').grid(row=7, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = f"{self.info['TEMPERATURE']} ℃").grid(row=7, column=1, sticky = 'ne')
        ttk.Label(self.frame_details_content, text = 'Min. Temperature : ').grid(row=8, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = f"{self.info['MIN_TEMPERATURE']} ℃").grid(row=8, column=1, sticky = 'ne')
        ttk.Label(self.frame_details_content, text = 'Max. Temperature : ').grid(row=9, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = f"{self.info['MAX_TEMPERATURE']} ℃").grid(row=9, column=1, sticky = 'ne')
        
        ttk.Label(self.frame_details_content, text = 'Visibility : ').grid(row=10, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = f"{self.info['VISIBILITY']} m").grid(row=10, column=1, sticky = 'ne')
        ttk.Label(self.frame_details_content, text = 'Pressure : ').grid(row=11, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = f"{self.info['PRESSURE']} hPa").grid(row=11, column=1, sticky = 'ne')
        ttk.Label(self.frame_details_content, text = 'Humidity : ').grid(row=12, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = f"{self.info['HUMIDITY']} %").grid(row=12, column=1, sticky = 'ne')
        ttk.Label(self.frame_details_content, text = 'Wind Speed : ').grid(row=13, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = f"{self.info['WIND_SPEED']} m/s").grid(row=13, column=1, sticky = 'ne')
        
        ttk.Label(self.frame_details_content, text = 'Time of Data Calculation : ').grid(row=14, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = f"{self.info['TDC']} UTC").grid(row=14, column=1, sticky = 'ne')
        ttk.Label(self.frame_details_content, text = 'Sun Rise : ').grid(row=15, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = f"{self.info['SUNRISE']} UTC").grid(row=15, column=1, sticky = 'ne')
        ttk.Label(self.frame_details_content, text = 'Sun Set : ').grid(row=16, column=0, sticky = 'nw')
        ttk.Label(self.frame_details_content, text = f"{self.info['SUNSET']} UTC").grid(row=16, column=1, sticky = 'ne')
        
        self.label_l_map = ttk.Label(self.frame_details_content, text = 'Here is the map:').grid(row=20, column=0, sticky = 'nw')
        self.mapButton = ttk.Button(self.frame_details_content, text = 'Map', command = self._makeMap).grid(row=20, column=1, sticky = 'ne')

    
    def _makeMap(self):
        
        loc = [self.info['LATITUDE'], self.info['LONGITUDE']]
        
        map_ = folium.Map(location = loc, zoom_start = 4)
        folium.Marker(loc, popup=self.info['CITY_NAME']).add_child(folium.features.CircleMarker(loc, radius = 3, color = 'blue', fill_color= 'blue')).add_to(map_)
            
        moment = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        map_name = f"{self._map_path}map{moment}.html"
        map_.save(map_name)
        
        webbrowser.get(self._chrome_path).open(map_name)

    def _submit_callback(self):
        # Data Validation Part
        try:
            tabnum = self.notebook.index(self.notebook.select())
            
            if tabnum == 0:
                if self.cntrycode.get().upper() not in self.ccvalue:
                    raise ValueError("Please select a country code in the list.")
                else:
                    checker= weather.WeatherCheckerCityCountry(self.entry_ctynm.get(), self.cntrycode.get())                
            elif tabnum == 1:
                checker= weather.WeatherCheckerCityID(self.entry_ctyid.get())
            else:           
                if float(self.entry_lat.get()) > 90 or float(self.entry_lat.get()) < -90:
                    raise ValueError("Latitude should be in the range from -90 to 90.")
                elif float(self.entry_lon.get()) > 180 or float(self.entry_lat.get()) < -180:
                    raise ValueError("Longitude should be in the range from -180 to 180.")
                else:
                    checker= weather.WeatherCheckerLonLat(self.entry_lon.get(), self.entry_lat.get())           
                    if checker.getCityID()==0:
                        raise ValueError("There is no record on these geographical coordinates.")

            self._pop_up_window(checker)
            
        except Exception as e:
            messagebox.showinfo(title='A Friendly Reminder', message=e)
        
    def _safe_close(self):
        for maphtml in os.listdir(self._map_path):
            if '.html' in maphtml:
                os.remove(maphtml)
        self.master.destroy()
        
def main():
    root = Tk()
    app = weatherApp(root)
    root.mainloop()
    
if __name__ == '__main__': main()