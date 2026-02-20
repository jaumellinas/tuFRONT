from django.shortcuts import render, redirect
from django.contrib import messages
from core import api_client
from core.api_client import APIError
from core.decorators import login_required, get_token


@login_required
def passatger_list(request):
    token = get_token(request)
    try:
        passatgers = api_client.get_passatgers(token)

        # Filtre de cerca
        cerca = request.GET.get('cerca', '').strip()
        if cerca:
            cerca_lower = cerca.lower()
            passatgers = [
                p for p in passatgers
                if (cerca_lower in p.get('nom', '').lower() or
                    cerca_lower in p.get('llinatge_1', '').lower() or
                    cerca_lower in p.get('llinatge_2', '').lower() or
                    cerca_lower in p.get('document', '').lower())
            ]
    except APIError as e:
        messages.error(request, e.detail)
        passatgers = []
    return render(request, "passatgers/list.html", {"passatgers": passatgers})


@login_required
def passatger_detail(request, passatger_id):
    token = get_token(request)
    try:
        passatger = api_client.get_passatger(token, passatger_id)
        targetes  = api_client.get_targetes_passatger(token, passatger_id)
    except APIError as e:
        messages.error(request, e.detail)
        return redirect("passatger_list")
    return render(request, "passatgers/detail.html", {
        "passatger": passatger,
        "targetes":  targetes,
    })


@login_required
def passatger_create(request):
    token = get_token(request)
    if request.method == "POST":
        data = {
            "nom":             request.POST.get("nom", "").strip(),
            "llinatge_1":      request.POST.get("llinatge_1", "").strip(),
            "llinatge_2":      request.POST.get("llinatge_2", "").strip() or None,
            "document":        request.POST.get("document", "").strip(),
            "email":           request.POST.get("email", "").strip(),
            "sessio_iniciada": False,
        }
        try:
            p = api_client.create_passatger(token, data)
            messages.success(request, "Passatger creat correctament.")
            return redirect("passatger_detail", passatger_id=p["id"])
        except APIError as e:
            messages.error(request, e.detail)

    return render(request, "passatgers/form.html", {"action": "Crear"})


@login_required
def passatger_edit(request, passatger_id):
    token = get_token(request)
    try:
        passatger = api_client.get_passatger(token, passatger_id)
    except APIError as e:
        messages.error(request, e.detail)
        return redirect("passatger_list")

    if request.method == "POST":
        data = {}
        for field in ("nom", "llinatge_1", "document", "email"):
            val = request.POST.get(field, "").strip()
            if val:
                data[field] = val
        llinatge_2 = request.POST.get("llinatge_2", "").strip()
        if llinatge_2:
            data["llinatge_2"] = llinatge_2

        try:
            api_client.update_passatger(token, passatger_id, data)
            messages.success(request, "Passatger actualitzat correctament.")
            return redirect("passatger_detail", passatger_id=passatger_id)
        except APIError as e:
            messages.error(request, e.detail)

    return render(request, "passatgers/form.html", {
        "action":    "Editar",
        "passatger": passatger,
    })


@login_required
def passatger_delete(request, passatger_id):
    token = get_token(request)
    if request.method == "POST":
        try:
            api_client.delete_passatger(token, passatger_id)
            messages.success(request, "Passatger eliminat correctament.")
        except APIError as e:
            messages.error(request, e.detail)
    return redirect("passatger_list")