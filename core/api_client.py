import requests
from django.conf import settings

BASE = settings.API_BASE_URL

## Excepcions i handlers

class APIError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def _headers(token: str | None = None) -> dict:
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _raise_for_status(response: requests.Response) -> dict:
    if response.status_code >= 400:
        try:
            detail = response.json().get("detail", response.text)
        except Exception:
            detail = response.text
        raise APIError(response.status_code, detail)
    if response.status_code == 204:
        return {}
    return response.json()


## Auth

def login_operador(email: str, password: str) -> dict:
    response = requests.post(
        f"{BASE}/api/v1/auth/token",
        data={"username": email, "password": password},
        headers={"Accept": "application/json"},
    )
    return _raise_for_status(response)




## Usuaris

def get_users(token: str, skip: int = 0, limit: int = None) -> list:
    params = {"skip": skip}
    if limit:
        params["limit"] = limit
    response = requests.get(
        f"{BASE}/api/v1/users",
        params=params,
        headers=_headers(token),
    )
    return _raise_for_status(response)


def get_user(token: str, user_id: int) -> dict:
    response = requests.get(
        f"{BASE}/api/v1/users/{user_id}",
        headers=_headers(token),
    )
    return _raise_for_status(response)


def get_me(token: str) -> dict:
    response = requests.get(
        f"{BASE}/api/v1/users/me",
        headers=_headers(token),
    )
    return _raise_for_status(response)


def create_user(token: str, data: dict) -> dict:
    response = requests.post(
        f"{BASE}/api/v1/users",
        json=data,
        headers=_headers(token),
    )
    return _raise_for_status(response)


def update_user(token: str, user_id: int, data: dict) -> dict:
    response = requests.put(
        f"{BASE}/api/v1/users/{user_id}",
        json=data,
        headers=_headers(token),
    )
    return _raise_for_status(response)


def delete_user(token: str, user_id: int) -> None:
    response = requests.delete(
        f"{BASE}/api/v1/users/{user_id}",
        headers=_headers(token),
    )
    _raise_for_status(response)


## Passatgers

def get_passatgers(token: str, skip: int = 0, limit: int = None) -> list:
    params = {"skip": skip}
    if limit:
        params["limit"] = limit
    response = requests.get(
        f"{BASE}/api/v1/passatgers",
        params=params,
        headers=_headers(token),
    )
    return _raise_for_status(response)


def get_passatger(token: str, passatger_id: int) -> dict:
    response = requests.get(
        f"{BASE}/api/v1/passatgers/{passatger_id}",
        headers=_headers(token),
    )
    return _raise_for_status(response)


def create_passatger(token: str, data: dict) -> dict:
    response = requests.post(
        f"{BASE}/api/v1/passatgers",
        json=data,
        headers=_headers(token),
    )
    return _raise_for_status(response)


def update_passatger(token: str, passatger_id: int, data: dict) -> dict:
    response = requests.put(
        f"{BASE}/api/v1/passatgers/{passatger_id}",
        json=data,
        headers=_headers(token),
    )
    return _raise_for_status(response)


def delete_passatger(token: str, passatger_id: int) -> None:
    response = requests.delete(
        f"{BASE}/api/v1/passatgers/{passatger_id}",
        headers=_headers(token),
    )
    _raise_for_status(response)


## Targetes

def get_targetes(token: str, skip: int = 0, limit: int = None) -> list:
    params = {"skip": skip}
    if limit:
        params["limit"] = limit
    response = requests.get(
        f"{BASE}/api/v1/targetes",
        params=params,
        headers=_headers(token),
    )
    return _raise_for_status(response)


def get_targeta(token: str, targeta_id: int) -> dict:
    response = requests.get(
        f"{BASE}/api/v1/targetes/{targeta_id}",
        headers=_headers(token),
    )
    return _raise_for_status(response)


def get_targetes_passatger(token: str, passatger_id: int) -> list:
    response = requests.get(
        f"{BASE}/api/v1/targetes/passatger/{passatger_id}",
        headers=_headers(token),
    )
    return _raise_for_status(response)


def create_targeta(token: str, data: dict) -> dict:
    response = requests.post(
        f"{BASE}/api/v1/targetes",
        json=data,
        headers=_headers(token),
    )
    return _raise_for_status(response)


def update_targeta(token: str, targeta_id: int, data: dict) -> dict:
    response = requests.put(
        f"{BASE}/api/v1/targetes/{targeta_id}",
        json=data,
        headers=_headers(token),
    )
    return _raise_for_status(response)