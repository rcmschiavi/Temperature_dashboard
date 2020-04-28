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
        with open(os.path.join(sys.path[0],"data.csv"),"a") as file: # Use file to refer to the file object
            file.write(str(data['temperatura'])+"\n")
        print("A temperatura é: {0}C".format(data['temperatura']))
        return HttpResponse("WOW!")
    else:
        test_file = open(os.path.join(sys.path[0],"data.csv"), 'rb')
        response = HttpResponse(content=test_file)
        response['Content-Type'] = 'text/csv'
        #response['Content-Disposition'] = 'attachment; filename='

        return response

