from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def cryptoApp(request):
    template = loader.get_template('message.html')
    return HttpResponse(template.render())