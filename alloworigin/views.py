from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response
from models import Request
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests
import json
from pytor import pytor


def index(request):
    return render_to_response('index.html')


@csrf_exempt
def get(request):
    if request.method in ['POST', 'GET']:
        url = request.GET.get('url', '')
        callback = request.GET.get('callback', '')
        tor = request.GET.get('tor', '')
        compress = request.GET.get('compress', '')

    # check valid url starts here
    if url != '':
        validate = URLValidator()
    else:
        return HttpResponse('invalid url')

    try:
        validate(url)
    except ValidationError:
        return HttpResponse('invalid url')
    # check valid url ends here

    # request
    try:
        if tor == '1':
            pytor_instance = pytor()
            try:
                # try to send tor request
                r = pytor_instance.get(url, timeout=3)
                origin = get_server_ip(tor='1', pytor_instance=pytor_instance)
            except Exception:
                # if tor not avail, use local instead
                r = requests.get(url, timeout=3)
                origin = get_server_ip()
        else:
            r = requests.get(url, timeout=3)
            origin = get_server_ip()

    except requests.exceptions.Timeout:
        return HttpResponse('timed out')

    this_request = Request(ip=get_client_ip(request), dest=url)
    this_request.save()

    if callback not in ['?', '']:
        if compress == '1':
            import zlib
            import base64
            response = JsonResponse(
                {"contents": base64.b64encode(zlib.compress(r.text)),
                 "status_code": r.status_code,
                 "origin": origin, "destination": url}
                )
        else:
            response = JsonResponse({"contents": r.text,
                                     "status_code": r.status_code,
                                     "origin": origin,
                                     "destination": url})
            return HttpResponse(callback+"("+response.content+")",
                                content_type="application/json")
    else:
        if compress == '1':
            import zlib
            import base64
            return JsonResponse(
                {"contents": base64.b64encode(zlib.compress(r.text)),
                 "status_code": r.status_code,
                 "origin": origin, "destination": url}
                )
        else:
            return JsonResponse(
                {"contents": r.text, "status_code": r.status_code,
                 "origin": origin, "destination": url}
                )


def get_server_ip(tor='0', pytor_instance='0'):
    url = 'https://api.ipify.org/?format=json'
    if tor == '0':
        origin = requests.get(url, timeout=3)
    else:
        origin = pytor_instance.get(url, timeout=3)
    origin = json.loads(origin.text)
    return origin['ip']


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
