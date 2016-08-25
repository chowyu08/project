from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.http import StreamingHttpResponse
import os
from backend.hotelSeeds import HotelSeeds
from backend.hotelList import HotelList
from backend.hotelType import HotelType
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def index(request):
    template = get_template('index.html')

    html = template.render({'request': request, })
    return HttpResponse(html)


def getSeeds(request, env, site, city):
    if(request.method != 'GET'):
        return
    hotelSeeds = HotelSeeds(env, site, city)
    return JSONResponse(hotelSeeds.get_seeds_url())


def getList(request, filename):
    if(request.method != 'GET'):
        return
    hotelList = HotelList(filename)
    return JSONResponse(hotelList.getList())


def getType(request, filename):
    if(request.method != 'GET'):
        return
    hotelType = HotelType(filename)
    return JSONResponse(hotelType.getResult())


def fileDownload(request, component, filename):
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    fullFileName = ""
    if component == "seed":
        fullFileName = './hotel/data/Seed/' + filename
    elif component == "list":
        fullFileName = './hotel/data/List/' + filename
    elif component == "type":
        fullFileName = './hotel/data/Type/' + filename
    else:
        return
    response = StreamingHttpResponse(file_iterator(fullFileName))
    response['Content-Type'] = 'application/octet-stream'
    response[
        'Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)

    return response
# hotelSeeds = HotelSeeds('ss', 'english', 'beijing')
# hotelSeeds.get_seeds_url()
