from django.urls import path
from core.views import dashboard
from core.views.auth import login, logout
from core.views.users import (
    user_list, user_detail, user_create, user_edit, user_delete,
)
from core.views.passatgers import (
    passatger_list, passatger_detail, passatger_create,
    passatger_edit, passatger_delete,
)
from core.views.targetes import (
    targeta_list, targeta_detail, targeta_create, targeta_edit,
)

urlpatterns = [

    # General
    path("",        dashboard, name="dashboard"),
    path("login/",  login,     name="login"),
    path("logout/", logout,    name="logout"),

    # Users
    path("users/",                               user_list,   name="user_list"),
    path("users/nou/",                           user_create, name="user_create"),
    path("users/<int:user_id>/",                 user_detail, name="user_detail"),
    path("users/<int:user_id>/editar/",          user_edit,   name="user_edit"),
    path("users/<int:user_id>/eliminar/",        user_delete, name="user_delete"),

    # Passatgers
    path("passatgers/",                                   passatger_list,   name="passatger_list"),
    path("passatgers/nou/",                               passatger_create, name="passatger_create"),
    path("passatgers/<int:passatger_id>/",                passatger_detail, name="passatger_detail"),
    path("passatgers/<int:passatger_id>/editar/",         passatger_edit,   name="passatger_edit"),
    path("passatgers/<int:passatger_id>/eliminar/",       passatger_delete, name="passatger_delete"),

    # Targetes
    path("targetes/",                            targeta_list,   name="targeta_list"),
    path("targetes/nova/",                       targeta_create, name="targeta_create"),
    path("targetes/<int:targeta_id>/",           targeta_detail, name="targeta_detail"),
    path("targetes/<int:targeta_id>/editar/",    targeta_edit,   name="targeta_edit"),
]