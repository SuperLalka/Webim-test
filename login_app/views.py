import random
import requests
from django.shortcuts import render, redirect
from urllib.parse import urlencode, unquote

from login_app import oauth


def index(request):
    if request.session.get('github_token'):
        return render(request, 'index.html')

    auth_params = {
        "client_id": oauth.GITHUB_CLIENT_KEY,
        "state": str(random.getrandbits(64)),
        "redirect_uri": oauth.REDIRECT_URI,
    }
    request.session['user_uniq_state'] = auth_params['state']
    return render(request, 'index.html', context={
        'github_auth': oauth.GITHUB_AUTHORIZE_URL,
        'auth_params': unquote(urlencode(auth_params)),
    })


def callback(request):
    if request.session['user_uniq_state'] == request.GET.get('state'):
        request.session.set_expiry(10000)

        auth_params = {
            "client_id": oauth.GITHUB_CLIENT_KEY,
            "client_secret": oauth.GITHUB_CLIENT_SECRET,
            "code": request.GET.get('code'),
            "state": str(random.getrandbits(64)),
            "redirect_uri": oauth.REDIRECT_URI,
        }

        response = requests.get(oauth.GITHUB_ACCESS_TOKEN,
                                headers={"Accept": "application/json"},
                                params={**auth_params})

        if response.ok:
            json_response = response.json()
            request.session['github_token'] = json_response['access_token']
        return redirect('/')


def logout(request):
    if request.session.get('github_token'):
        del request.session['github_token']
    return redirect('/')
