from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response
from models import Request
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests

@csrf_exempt
def index(request):
    if request.method == 'GET':
        url = request.GET.get('url', '')
    if request.method == 'POST':
        url = request.POST.get('url', '')
    if url != '':
        validate = URLValidator()
        try:
            validate(url)
            r = requests.get(url)
            this_request = Request(ip=get_client_ip(request),dest=url)
            this_request.save()
            return JsonResponse({"contents":r.text,"status_code":r.status_code})
        except ValidationError, Exception:
            return HttpResponse('invalid url')
    return render_to_response('index.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip