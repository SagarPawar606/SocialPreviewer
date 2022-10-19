import csv
from urllib import response

from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .utils import get_meta_data

# Create your views here.

downloadable_meta_data = None

def index(request):
    url = request.GET.get('url')
    if url:
        data = get_meta_data(url)
        if not data:
            messages.error(request, 'No such URL found ! Please try again.')
        else:
            global downloadable_meta_data
            downloadable_meta_data = data

            context = {'tag' : data}
            return render(request, 'main_app/index.html', context)
    return render(request, 'main_app/index.html')

def social_api(request):
    url = request.GET['url']
    if request.method == 'GET':
        data = get_meta_data(url)
        if not data:
            return JsonResponse({'status':'false', 'message':'Not a valid url'}, status=400)
        return JsonResponse(data, status=200)

def download_meta(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="socialpreviewer.csv"'

    fieldnames = ['Tag', 'Data']
    writer = csv.DictWriter(response, fieldnames=fieldnames)

    writer.writeheader()
    for key, value in downloadable_meta_data.items():
        writer.writerow({'Tag':key, 'Data':value})

    return response

        
