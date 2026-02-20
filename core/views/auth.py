from django.shortcuts import render, redirect
from django.contrib import messages
from core import api_client
from core.api_client import APIError


def login(request):
    if request.session.get("token"):
        return redirect("dashboard")

    if request.method == "POST":
        email    = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        try:
            data = api_client.login_operador(email, password)
            request.session["token"] = data["access_token"]
            request.session["email"] = email
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
        except APIError as e:
            messages.error(request, e.detail)

    return render(request, "auth/login.html")


def logout(request):
    request.session.flush()
    messages.success(request, "Sessió tancada correctament.")
    return redirect("login")