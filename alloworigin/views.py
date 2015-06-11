from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response
from models import Request
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests


def index(request):
    return render_to_response('index.html')

@csrf_exempt
def get(request):
    if request.method == 'GET':
        url = request.GET.get('url', '')
    if request.method == 'POST':
        url = request.POST.get('url', '')
    if url != '':
        validate = URLValidator()
    else:
        return HttpResponse('invalid url')        
    try:
        r = requests.get(url,timeout=5)
    except requests.exceptions.Timeout:
        return HttpResponse('timed out')
    try:
        validate(url)
        this_request = Request(ip=get_client_ip(request),dest=url)
        this_request.save()
        return JsonResponse({"contents":r.text,"status_code":r.status_code})
    except ValidationError, Exception:
        return HttpResponse('invalid url')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
