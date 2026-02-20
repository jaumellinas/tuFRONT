from django.shortcuts import render
from django.contrib import messages
from core import api_client
from core.api_client import APIError
from core.decorators import login_required, get_token


@login_required
def dashboard(request):
    token = get_token(request)
    context = {}
    try:
        context["num_passatgers"] = len(api_client.get_passatgers(token))
        context["num_targetes"]   = len(api_client.get_targetes(token))
        context["num_users"]      = len(api_client.get_users(token))
        context["perfil"]         = api_client.get_me(token)
    except APIError as e:
        messages.error(request, f"Error carregant el tauler: {e.detail}")
    return render(request, "dashboard.html", context)