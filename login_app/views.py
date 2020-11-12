import random
import requests
from django.shortcuts import render
from urllib.parse import urlencode, unquote

from login_app import oauth


def index(request):
    if request.GET.get('code'):
        request.session['user_code'] = request.GET.get('code')
    auth_params = {
        "response_type": "code",
        "client_id": oauth.CLIENT_KEY,
        "redirect_uri": oauth.REDIRECT_URI,
    }
    return render(request, 'index.html', context={'auth_params': unquote(urlencode(auth_params))})


def auth(request):
    auth_params = {
        "client_id": oauth.CLIENT_KEY,
        "state": str(random.getrandbits(64)),
        "redirect_uri": oauth.REDIRECT_URI,
        "response_type": "code",
        "code": request.session['user_code'],
    }
    response = requests.post(
        oauth.GITHUB_AUTHORIZE_URL,
        json={**auth_params}
    )
    print(response)
    return response
