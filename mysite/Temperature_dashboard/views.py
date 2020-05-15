# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.views.decorators .csrf import csrf_exempt
from django.http import JsonResponse
from .models import Temperature
from django.utils import timezone
import datetime
import pandas as pd
import numpy as np
import pytz

import csv
import json
import os
import sys

tz = pytz.timezone('America/Caracas')

def index(request):
    return render(request, 'index.html')
# Create your views here.


@csrf_exempt
def post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        temp = data['temperatura']
        try:
            HASH = data['HASH']
        except:
            HASH = ""
        if(HASH == "HA3958KTPrs9*#8"): # A HASH provided by the devices to avoid users to create posts
            with open(os.path.join(sys.path[0],"data.csv"),"a") as file: # Use file to refer to the file object
                file.write(str(temp)+"\n")
            dataDB = Temperature(TEMPERATURE = temp)
            dataDB.save()
            print("A temperatura é: {0}C".format(data['temperatura']))

            return HttpResponse("PERFECT!")
        else:
            print("The device haven't provide the right HASH.")
            return HttpResponse("You haven't provide the right HASH.")
    else:
        test_file = open(os.path.join(sys.path[0],"data.csv"), 'rb')
        response = HttpResponse(content=test_file)
        response['Content-Type'] = 'text/csv'
        #response['Content-Disposition'] = 'attachment; filename='

        return response

def temperature_chart_view(request):
    timezone.now()
    listData = get_temp_by_hour()
    context = {
        'listData': listData
    }
    return render(request, 'temperature_chart.html', context)

def update_chart(request):
    date_handler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, (datetime.datetime, datetime.date))
        else None
    )
    query = Temperature.objects.order_by('-REGISTERED_AT').first()
    context = {
        'temp': query.TEMPERATURE,
        'time': query.REGISTERED_AT.astimezone(tz).__format__('%c')
    }
    #print("Chamou:" + str(context))
    return JsonResponse(context)


def get_temp_by_hour():
    global tz
    date = datetime.datetime.now(tz)
    day = int(date.strftime("%d"))
    month = int(date.strftime("%m"))
    year = int(date.strftime("%Y"))
    # A complete query that returns just the values from the current day
    dataset = Temperature.objects.order_by('-REGISTERED_AT').filter(REGISTERED_AT__range=(
                                            datetime.datetime(year, month, day, tzinfo=pytz.UTC),
                                            datetime.datetime(year, month, day, tzinfo=pytz.UTC) +
                                            datetime.timedelta(days=1))).exclude(TEMPERATURE__lte=-120).values('TEMPERATURE', 'REGISTERED_AT')

    df = pd.DataFrame(list(dataset))
    df.REGISTERED_AT = pd.to_datetime(df.REGISTERED_AT)
    df.REGISTERED_AT = df.REGISTERED_AT.dt.tz_convert('America/Caracas')
    df.TEMPERATURE = df.TEMPERATURE.astype(float)
    hour = pd.to_timedelta(df.REGISTERED_AT.dt.hour, unit='H')
    hour.name = "REGISTERED_AT"
    df2 = df.groupby(hour).mean()
    listData = format_data(df, df2)
    df2.index = df2.index.astype(str)
    df2.TEMPERATURE = df2.TEMPERATURE.round(2)
    return listData

def filter_date(df, year,month,day):
    print("Len antes: " + str(len(df)))
    df = df[df.REGISTERED_AT.dt.year==year]
    df = df[df.REGISTERED_AT.dt.month==month]
    df = df[df.REGISTERED_AT.dt.day==day]
    print("Len depois: " + str(len(df)))
    return df

def format_data(df, df2):
    dataDict: {}
    listData = []
    for hour in df2.index:
        a = np.timedelta64(hour.to_numpy(), 'ns')
        a = int(a/3600000000000)
        df3 = df[df.REGISTERED_AT.dt.hour == a]
        dataDict = {"v":[a,0,0],"f":"Time: "+  str(a)+":00"}
        listHour = [dataDict, df3.max().TEMPERATURE,df3.mean().round(2).TEMPERATURE,df3.min().TEMPERATURE]
        listData.append(listHour)
    return listData