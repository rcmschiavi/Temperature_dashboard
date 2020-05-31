import datetime
import json
import time
import pytz
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import numpy as np
from .models import Agriculture_data


def application_page(request):
    get_data_models()
    context = {
        'listData': get_data_models()[0],
        'execution_time': get_data_models()[1]
    }
    return render(request, 'my_plant.html', context)


def get_data_models():
    start_time = time.time()
    tz = pytz.timezone('America/Porto_Velho')
    date = datetime.datetime.now(tz)
    day = date.day
    month = date.month
    year = date.year
    dataset = Agriculture_data.objects.order_by('-REGISTERED_AT').\
        filter(REGISTERED_AT__gte=datetime.datetime(year, month, 28, tzinfo=tz)).\
        values('TEMPERATURE', 'REGISTERED_AT', 'HUMIDITY', 'MOISTURE')
    df = pd.DataFrame(list(dataset))
    df.REGISTERED_AT = pd.to_datetime(df.REGISTERED_AT)
    df.REGISTERED_AT = df.REGISTERED_AT.dt.tz_convert('America/Caracas')
    df.TEMPERATURE = df.TEMPERATURE.astype(float)
    df.HUMIDITY = df.HUMIDITY.astype(float)
    df.MOISTURE = df.MOISTURE.astype(float)
    hour = pd.to_timedelta(df.REGISTERED_AT.dt.hour, unit='H')
    hour.name = "REGISTERED_AT"
    df = df.groupby(hour).mean().round(2)
    return format_data(df),(start_time - time.time())


def format_data(df):
    # Function to format the data for google charts data format, also got the max and min temperature
    data_dict: {}
    list_data = []
    NS_IN_ONE_HOUR = 3600000000000
    for index, row in df.iterrows():
        delta_hour = np.timedelta64(index.to_numpy(), 'ns')
        delta_hour = int(delta_hour / NS_IN_ONE_HOUR)
        list_hour = [[delta_hour, 0, 0], row['TEMPERATURE'], row['HUMIDITY'], row['MOISTURE']]
        list_data.append(list_hour)
    return list_data


@csrf_exempt
def post_agriculture_data(request):

    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        try:
            post_hash = data['HASH']
        except KeyError:
            return HttpResponse("The data is not complete.")
        except Exception as e:
            return HttpResponse("Some error occured during the post. Exception: " + str(e))

        # A HASH provided by the devices to avoid users to create posts
        if post_hash == settings.SENSOR_HASH_POSTING:
            temp = data['temperatura']
            humidity = data['umidade']
            moisture = data['umidade_solo']
            data_db = Agriculture_data(TEMPERATURE=temp, HUMIDITY=humidity, MOISTURE=moisture)
            data_db.save()
            print("A temperatura é: {0}C, a umidade é: {1} e a umidade do solo eh: {2}".format(temp,humidity,moisture))

            return HttpResponse(200)
        else:
            return HttpResponse("You haven't provide the right HASH.")


def update_agriculture(request):
    tz = pytz.timezone('America/Porto_Velho')

    query = Agriculture_data.objects.order_by('-REGISTERED_AT').first()
    context = {'temp': query.TEMPERATURE,
               'humidity': query.HUMIDITY,
               'moisture': query.MOISTURE,
                'time': query.REGISTERED_AT.astimezone(tz).__format__('%c')

    }
    return JsonResponse(context)
