from django.shortcuts import render, redirect
from django.contrib import messages
from core import api_client
from core.api_client import APIError
from core.decorators import login_required, get_token


@login_required
def user_list(request):
    token = get_token(request)
    try:
        users = api_client.get_users(token)
    except APIError as e:
        messages.error(request, e.detail)
        users = []
    return render(request, "users/list.html", {"users": users})


@login_required
def user_detail(request, user_id):
    token = get_token(request)
    try:
        user = api_client.get_user(token, user_id)
    except APIError as e:
        messages.error(request, e.detail)
        return redirect("user_list")
    return render(request, "users/detail.html", {"user": user})


@login_required
def user_create(request):
    token = get_token(request)
    if request.method == "POST":
        data = {
            "nom":        request.POST.get("nom", "").strip(),
            "llinatge_1": request.POST.get("llinatge_1", "").strip(),
            "llinatge_2": request.POST.get("llinatge_2", "").strip() or None,
            "email":      request.POST.get("email", "").strip(),
            "password":   request.POST.get("password", ""),
        }
        try:
            api_client.create_user(token, data)
            messages.success(request, "Usuari creat correctament.")
            return redirect("user_list")
        except APIError as e:
            messages.error(request, e.detail)

    return render(request, "users/form.html", {"action": "Crear"})


@login_required
def user_edit(request, user_id):
    token = get_token(request)
    try:
        user = api_client.get_user(token, user_id)
    except APIError as e:
        messages.error(request, e.detail)
        return redirect("user_list")

    if request.method == "POST":
        data = {}
        for field in ("nom", "llinatge_1", "email"):
            val = request.POST.get(field, "").strip()
            if val:
                data[field] = val
        llinatge_2 = request.POST.get("llinatge_2", "").strip()
        if llinatge_2:
            data["llinatge_2"] = llinatge_2
        password = request.POST.get("password", "")
        if password:
            data["password"] = password

        try:
            api_client.update_user(token, user_id, data)
            messages.success(request, "Usuari actualitzat correctament.")
            return redirect("user_list")
        except APIError as e:
            messages.error(request, e.detail)

    return render(request, "users/form.html", {"action": "Editar", "user": user})


@login_required
def user_delete(request, user_id):
    token = get_token(request)
    if request.method == "POST":
        try:
            api_client.delete_user(token, user_id)
            messages.success(request, "Usuari eliminat correctament.")
        except APIError as e:
            messages.error(request, e.detail)
    return redirect("user_list")