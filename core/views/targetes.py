from django.shortcuts import render, redirect
from django.contrib import messages
from core import api_client
from core.api_client import APIError
from core.decorators import login_required, get_token

PERFILS = ["General", "Jove", "Infantil", "Pensionista", "Altres"]
ESTATS = ["Activa", "Robada", "Caducada", "Perduda", "Desactivada", "Altres"]


@login_required
def targeta_list(request):
    token = get_token(request)
    try:
        targetes = api_client.get_targetes(token)

        # Filtre de cerca per codi de targeta
        cerca = request.GET.get('cerca', '').strip()
        if cerca:
            cerca_lower = cerca.lower()
            targetes = [
                t for t in targetes
                if cerca_lower in t.get('codi_targeta', '').lower()
            ]
    except APIError as e:
        messages.error(request, e.detail)
        targetes = []
    return render(request, "targetes/list.html", {"targetes": targetes})


@login_required
def targeta_detail(request, targeta_id):
    token = get_token(request)
    try:
        targeta = api_client.get_targeta(token, targeta_id)
        passatger = api_client.get_passatger(token, targeta['id_passatger'])
    except APIError as e:
        messages.error(request, e.detail)
        return redirect("targeta_list")
    return render(request, "targetes/detail.html", {
        "targeta": targeta,
        "passatger": passatger
    })


@login_required
def targeta_create(request):
    token = get_token(request)

    try:
        passatgers = api_client.get_passatgers(token)
    except APIError:
        passatgers = []

    passatger_preseleccionat = None
    if request.GET.get('passatger_id'):
        try:
            passatger_preseleccionat = int(request.GET.get('passatger_id'))
        except ValueError:
            pass

    if request.method == "POST":
        saldo_raw = request.POST.get("saldo", "0").strip()
        data = {
            "id_passatger": int(request.POST.get("id_passatger")),
            "perfil": request.POST.get("perfil"),
            "saldo": saldo_raw,
            "estat": request.POST.get("estat", "Activa"),
        }
        try:
            t = api_client.create_targeta(token, data)
            messages.success(
                request,
                f"Targeta creada correctament amb codi {t['codi_targeta']}."
            )
            return redirect("targeta_detail", targeta_id=t["id"])
        except APIError as e:
            messages.error(request, e.detail)

    return render(request, "targetes/form.html", {
        "action": "Crear",
        "passatgers": passatgers,
        "passatger_preseleccionat": passatger_preseleccionat,
        "perfils": PERFILS,
        "estats": ESTATS,
    })


@login_required
def targeta_edit(request, targeta_id):
    token = get_token(request)
    try:
        targeta = api_client.get_targeta(token, targeta_id)
    except APIError as e:
        messages.error(request, e.detail)
        return redirect("targeta_list")

    if request.method == "POST":
        data = {}
        saldo = request.POST.get("saldo", "").strip()
        estat = request.POST.get("estat", "").strip()
        if saldo:
            data["saldo"] = saldo
        if estat:
            data["estat"] = estat

        try:
            api_client.update_targeta(token, targeta_id, data)
            messages.success(request, "Targeta actualitzada correctament.")
            return redirect("targeta_detail", targeta_id=targeta_id)
        except APIError as e:
            messages.error(request, e.detail)

    return render(request, "targetes/form.html", {
        "action":  "Editar",
        "targeta": targeta,
        "estats":  ESTATS,
    })