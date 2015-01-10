from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


def home(request):
    return render(request, 'index.html', {
        'api_converter_url': 'http://127.0.0.1:8000/api/v1.0/converter/',
        'api_youtube_converter_url': 'http://127.0.0.1:8000/api/v1.0/youtube-converter/',
    })