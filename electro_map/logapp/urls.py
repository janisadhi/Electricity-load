from django.urls import path
from django.urls import path
from django.urls import path
from .views import power_allocation
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(power_allocation), name='power_allocation'),
]
