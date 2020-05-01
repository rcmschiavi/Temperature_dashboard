# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.views.decorators .csrf import csrf_exempt
from django.http import JsonResponse
from .models import Temperature
import datetime
import pandas as pd

import csv
import json
import os
import sys

def index(request):
    return HttpResponse("<h1>HEEEY</h1>")
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

def page(request):
    names = ["AA", "BBB", "CCC"]
    prices = [10,5,14]
    context = {
        'names': json.dumps(names),
        'prices': json.dumps(prices),
    }
    return render(request, 'Temperature_dashboard/dashboard.html',context)

#def vue_test(request):


def temperature_chart_view(request):
    date = []
    data = []
    date_handler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, (datetime.datetime, datetime.date))
        else None
    )
    queryset = Temperature.objects.order_by('-REGISTERED_AT').values('TEMPERATURE','REGISTERED_AT')
    date, data = get_temp_hour(queryset)
    context = {
        'names': date,
        'prices': data,
    }
    print(context)
    return render(request, 'Temperature_dashboard/dashboard.html', context)

def update_chart(request):
    date = []
    data = []
    date_handler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, (datetime.datetime, datetime.date))
        else None
    )
    query = Temperature.objects.order_by('-REGISTERED_AT')[0]
    context = {
        'temp': query.TEMPERATURE,
        'time': query.REGISTERED_AT
    }
    #print("Chamou:" + str(context))
    return JsonResponse(context)


def get_temp_hour(dataset):
    df = pd.DataFrame(list(dataset))
    df.REGISTERED_AT = pd.to_datetime(df.REGISTERED_AT)
    print(df.head())
    df.TEMPERATURE = df.TEMPERATURE.astype(float)
    hour = pd.to_timedelta(df.REGISTERED_AT.dt.hour, unit='H')
    hour.name = "REGISTERED_AT"
    print(df.head())
    df = df.groupby(hour).mean()
    df.index = df.index.astype(str)
    print(df)
    return list(df.index[:24]),list(df.TEMPERATURE[:24])
