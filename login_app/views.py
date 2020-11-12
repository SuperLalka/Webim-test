import random
from django.http import HttpResponse
from django.shortcuts import render
from urllib.parse import urlencode, unquote

from login_app import oauth


def index(request):
    auth_params = {
        "client_id": oauth.GITHUB_CLIENT_KEY,
        "state": str(random.getrandbits(64)),
        "redirect_uri": oauth.REDIRECT_URI,
    }
    return render(request, 'index.html', context={
        'github_auth': oauth.GITHUB_AUTHORIZE_URL,
        'auth_params': unquote(urlencode(auth_params)),
    })


def callback(request):
    request.session['user_code'] = request.GET.get('code')
    request.session.set_expiry(10000)
    return HttpResponse(request)
