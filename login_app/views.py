import random
import requests
from django.shortcuts import render, redirect
from urllib.parse import urlencode, unquote

from django.conf import settings


def index(request):
    """
    Renders the main page based on the presence
    of a token for authorization in the user session
    """
    if request.session.get('github_token'):
        return render(request, 'index.html')

    auth_params = {
        "client_id": settings.GITHUB_CLIENT_KEY,
        "state": str(random.getrandbits(64)),
        "redirect_uri": settings.OAUTH_REDIRECT_URI,
    }
    request.session['user_uniq_state'] = auth_params['state']
    return render(request, 'index.html', context={
        'github_auth': settings.GITHUB_AUTHORIZE_URL,
        'auth_params': unquote(urlencode(auth_params)),
    })


def callback(request):
    """
    Сalled when the authorization from Github responds,
    checks against the sent 'state' and exchanges
    the received code to the token that is saved in the session
    """
    if request.session['user_uniq_state'] == request.GET.get('state'):
        request.session.set_expiry(10000)

        auth_params = {
            "client_id": settings.GITHUB_CLIENT_KEY,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": request.GET.get('code'),
            "redirect_uri": settings.OAUTH_REDIRECT_URI,
        }

        response = requests.get(settings.GITHUB_ACCESS_TOKEN,
                                headers={"Accept": "application/json"},
                                params={**auth_params})

        if response.ok:
            json_response = response.json()
            request.session['github_token'] = json_response['access_token']
    return redirect('/')


def logout(request):
    """
    Removes token from session
    """
    if request.session.get('github_token'):
        del request.session['github_token']
    return redirect('/')
