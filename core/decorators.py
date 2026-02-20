from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

# Bloqueja l'accés a una pàgina si no troba una cookie de sessió vàlida

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("token"):
            messages.warning(request, "Has d'iniciar sessió per accedir a aquesta pàgina.")
            next_url = request.get_full_path()
            return redirect(f"/login?next={next_url}")
        return view_func(request, *args, **kwargs)
    return wrapper


def get_token(request) -> str:
    return request.session.get("token", "")