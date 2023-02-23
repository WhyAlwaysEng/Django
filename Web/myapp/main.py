import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt
import numpy as np
import socket
from ftplib import FTP_TLS
import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import datetime
import folium
import webbrowser

def getfileFTP():
    host = '188.166.217.51'
    port = 7021
    usr = 'tung'
    pwd = 'anundaJJ795'
    ftp = FTP_TLS()
    ftp.connect(host, port)
    ftp.login(usr, pwd)
    ftp.cwd("/BER/")

    files = ftp.nlst()
    print("iifjioerfjioerfjioejrfoierjfoierjfioerjfioejofjerofijeorijfieorjfioerjfioeriorvjio3fjp")
    files.sort(key=lambda x: ftp.sendcmd("MDTM " + x)[4:])
    print(files)
    latest_file = files[-1]
    with open(latest_file, "wb") as f:
        ftp.retrbinary(f"RETR {latest_file}", f.write)

    print(latest_file)
    ftp.quit()
    return latest_file


def getdata(latest_file):
    # Open the file and read the data
    with open(latest_file, 'r') as file:
        data = file.read()

    # Split the data into individual JSON objects
    data_list = data.strip().split('\n')
    # print(data_list)
    # Extract the required data
    temp_list = []
    humi_list = []
    time_list = []
    lat_list =[]
    lon_list = []
    date_list = []
    Batt_Lev_list = []
    time_new = []
    temp_new = []
    humi_new = []
    lat_new =[]
    lon_new = []
    date_new = []
    Batt_Lev_new = []
    offset = timedelta(hours=7)
    i=0
    for item in data_list:
        json_data = json.loads(item)
        temp_list.append(str(float(json_data['Temp'])))
        humi_list.append(float(json_data['Humi']))
        lat_list.append(json_data['Lat'])
        lon_list.append(json_data['Lon'])
        Batt_Lev_list.append(json_data['Batt_Lev'])
        date_str=json_data['Date']
        time_str=json_data['Time']
        full_time = datetime.strptime(date_str + ' ' + time_str, '%Y/%m/%d %H:%M:%S')
        full_time_gmt7 = full_time+offset
        date_str = (full_time_gmt7.date()).strftime('%Y/%m/%d')
        time_str = (full_time_gmt7.time()).strftime('%H:%M:%S')
        if lon_list[i] is None:
            lon_list[i] = lon_list[i-1]
            print("Latitude is None, using previous value.")
        if lat_list[i] is None:
            lat_list[i] = lat_list[i-1]
            print("Latitude is None, using previous value.")
        date_list.append(date_str)
        time_list.append(time_str)
        i=i+1

        
    if len(date_list) > 20:
        size = len(date_list)
        index = size-20
        print(index)
        for k in range(20):
            time_new.append(time_list[index])
            temp_new.append(temp_list[index])
            humi_new.append(humi_list[index])
            lat_new.append(lat_list[index])
            lon_new.append(lon_list[index])
            date_new.append(date_list[index])
            Batt_Lev_new.append(Batt_Lev_list[index])
            index=index+1
        temp_list=temp_new
        humi_list=humi_new
        lat_list=lat_new
        lon_list=lon_new
        date_list=date_new
        Batt_Lev_list=Batt_Lev_new
        time_list=time_new


    print("Date = "+str(date_list))
    print("Time = "+str(time_list))
    print(Batt_Lev_list[0])
    return temp_list,humi_list,time_list,lat_list,lon_list,date_list,Batt_Lev_list


def plotdata(temp_list,humi_list,time_list,lat_list,lon_list,date_list):
    temp_list_float=[]
    for i in range(np.size(temp_list)):
        temp_list_float.append(float(temp_list[i]))
    
    plt.figure(figsize=(15,6))
    plt.suptitle("Temperature (°C) between "+time_list[0]+" to "+time_list[-1],fontsize=14)
    plt.xticks(rotation=45)
    plt.plot(time_list,temp_list_float, "o-")
    plt.grid()
    plt.xlabel("Time")
    plt.ylim([-40,100])
    plt.ylabel("Temperature (°C)")
    plt.savefig("graph1.png")
    plt.figure(figsize=(15,6 ))
    plt.suptitle("Humidity (%) between "+time_list[0]+" to "+time_list[-1],fontsize=18)
    plt.xticks(rotation=45)
    plt.plot(time_list,humi_list, "o-")
    plt.grid()
    plt.xlabel("Time")
    plt.ylim([0,100])
    plt.ylabel("Humidity (%)")
    plt.savefig("graph2.png")
    # plt.tight_layout()
    # plt.subplot(1,2,2)
    # plt.xticks(rotation=45)
    # plt.plot(time_list,humi_list, "o-")
    # plt.grid()
    # plt.xlabel("Time")
    # plt.ylim([0,100])
    # plt.ylabel("Humidity (%)")
    # plt.tight_layout()
    # plt.savefig("graph.png")


def plotmap(temp_list,humi_list,time_list,lat_list,lon_list,date_list):
    fg= folium.FeatureGroup(name="Thailand")
    for i in range (np.size(lat_list)):
        if (lat_list[i]=="" or lon_list[i]==""):
            lat_list[i]=lat_list[i-1]
            lon_list[i]=lon_list[i-1]
        fg.add_child(folium.Marker(
            location=[lat_list[i],lon_list[i]],
            title = time_list[i]   
        ))

    lat_avg = sum([float(x) for x in lat_list])/np.size(lat_list)
    lon_avg = sum([float(x) for x in lon_list])/np.size(lat_list)
    map = folium.Map(location=(lat_avg, lon_avg), zoom_start=12)
    map.add_child(fg)
    map.save("map.html")

def findavg(temp_list,humi_list):
    temp_avg = sum([float(x) for x in temp_list])/np.size(temp_list)
    temp_avg = "{:.2f}".format(temp_avg)
    humi_avg = sum([float(x) for x in humi_list])/np.size(humi_list)
    humi_avg = "{:.2f}".format(humi_avg)
    return temp_avg,humi_avg