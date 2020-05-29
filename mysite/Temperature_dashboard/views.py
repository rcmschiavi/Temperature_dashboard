# coding: utf-8
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from . import get_temperature_observatory as get_temp
from .models import Temperature
from django.utils import timezone
from django.conf import settings
import datetime
import pandas as pd
import numpy as np
import pytz
import json

def index(request): return render(request, 'index.html')


def resume(request):

    with open(os.path.join(settings.BASE_DIR, 'assets/files/resume.pdf'), 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=resume.pdf'
        return response

@csrf_exempt
def post_temperature(request):

    if request.method == "POST":
        data = json.loads(request.body)

        try:
            post_hash = data['HASH']
        except KeyError:
            return HttpResponse("The data is not complete.")
        except Exception as e:
            return HttpResponse("Some error occured during the post. Exception: " + str(e))

        # A HASH provided by the devices to avoid users to create posts
        if post_hash == settings.SENSOR_HASH_POSTING:
            temp = data['temperatura']
            try:
                temp_observatory, time_observatory = get_temp.get_json()
                data_db = Temperature(TEMPERATURE=temp, TEMPERATURE_OBSERVATORY=temp_observatory,
                                      TIME_OBSERVATORY=time_observatory)
            except:
                data_db = Temperature(TEMPERATURE=temp)
            data_db.save()
            print("A temperatura é: {0}C".format(data['temperatura']))

            return HttpResponse(200)
        else:
            return HttpResponse("You haven't provide the right HASH.")


def temperature_chart_view(request):
    timezone.now()
    list_data = get_temp_by_hour()
    print(list_data)
    context = {
        'listData': list_data
    }
    return render(request, 'temperature_chart.html', context)


def update_chart(request):
    tz = pytz.timezone('America/Porto_Velho')
    query = Temperature.objects.order_by('-REGISTERED_AT').first()
    context = {
        "My_data":{'temp': query.TEMPERATURE,
                   'time': query.REGISTERED_AT.astimezone(tz).__format__('%c')
                   },
        "Observatory_data":{'temp': query.TEMPERATURE_OBSERVATORY,
                            'time': query.TIME_OBSERVATORY.astimezone(tz).__format__('%c')
                            }
    }
    return JsonResponse(context)


def get_temp_by_hour():
    tz = pytz.timezone('America/Porto_Velho')
    date = datetime.datetime.now(tz)
    day = date.day
    month = date.month
    year = date.year
    # A complete query that returns just the values from the current day
    dataset = Temperature.objects.order_by('-REGISTERED_AT') \
        .filter(REGISTERED_AT__gte=datetime.datetime(year, month, day, tzinfo=tz)) \
        .exclude(TEMPERATURE__lte=-120).values('TEMPERATURE', 'REGISTERED_AT')
    df = pd.DataFrame(list(dataset))
    df.REGISTERED_AT = pd.to_datetime(df.REGISTERED_AT)
    df.REGISTERED_AT = df.REGISTERED_AT.dt.tz_convert('America/Caracas')
    df.TEMPERATURE = df.TEMPERATURE.astype(float)
    hour = pd.to_timedelta(df.REGISTERED_AT.dt.hour, unit='H')
    hour.name = "REGISTERED_AT"
    df2 = df.groupby(hour).mean()
    listData = format_data(df, df2)
    return listData


def format_data(df, df2):
    # Function to format the data for google charts data format, also got the max and min temperature
    data_dict: {}
    list_data = []
    NS_IN_ONE_HOUR = 3600000000000
    for hour in df2.index:
        delta_hour = np.timedelta64(hour.to_numpy(), 'ns')
        delta_hour = int(delta_hour / NS_IN_ONE_HOUR)
        df_hour = df[df.REGISTERED_AT.dt.hour == delta_hour]
        data_dict = {"v": [delta_hour, 0, 0], "f": "Time: " + str(delta_hour) + ":00"}
        list_hour = [data_dict, df_hour.max().TEMPERATURE, df_hour.mean().round(2).TEMPERATURE, df_hour.min().TEMPERATURE]
        list_data.append(list_hour)
    return list_data
