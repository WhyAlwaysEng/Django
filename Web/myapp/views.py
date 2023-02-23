from django.shortcuts import render
from django.http import HttpResponse
from . import main
# Create your views here.


def index(request):
    filefromftp =main.getfileFTP()
    temp_list,humi_list,time_list,lat_list,lon_list,date_list,Batt_Lev_list = main.getdata(filefromftp)
    main.plotdata(temp_list,humi_list,time_list,lat_list,lon_list,date_list)
    main.plotmap(temp_list,humi_list,time_list,lat_list,lon_list,date_list)
    temp_avg,humi_avg = main.findavg(temp_list,humi_list)
    Batt=Batt_Lev_list[-1]
    temp = temp_list[-1]
    humi = humi_list[-1]
    humi="{:.2f}".format(humi)
    lastupdate = str(date_list[-1])+" "+str(time_list[-1])

    return render(request,'index.html',{"temp":temp,"humi":humi,"tempavg":temp_avg,"humiavg":humi_avg,"Batt_Lev":Batt,"Time":lastupdate})

def BER(request):



    return render(request,'BER.html')