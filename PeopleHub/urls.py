from django.contrib import admin
from django.http import JsonResponse
from django.urls import path


def index(request):
    return JsonResponse({"message": "PeopleHub is running"})


urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
]
