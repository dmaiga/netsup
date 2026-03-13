from django.urls import path
from users.views import *

urlpatterns = [

    path("dashboard/superviseur/", dashboard_superviseur, name="dashboard_superviseur"),
    path("dashboard/admin/", dashboard_admin, name="dashboard_admin"),

    path('list/', user_list, name='user_list'),
    path("detail/<int:pk>/", user_detail, name="user_detail"),
    path('create/', user_create, name='user_create'),
    path('update/<int:pk>/', user_update, name='user_update'),

    path('toggle/<int:pk>/', user_toggle_active, name='user_toggle'),
    path('delete/<int:pk>/', user_soft_delete, name='user_delete'),
]