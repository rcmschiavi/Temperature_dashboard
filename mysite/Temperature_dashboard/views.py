# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.views.decorators .csrf import csrf_exempt
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
        try:
            HASH = data['HASH']
        except:
            HASH = ""
        if(HASH == "HA3958KTPrs9*#8"): # A HASH provided by the devices to avoid users to create posts
            with open(os.path.join(sys.path[0],"data.csv"),"a") as file: # Use file to refer to the file object
                file.write(str(data['temperatura'])+"\n")
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