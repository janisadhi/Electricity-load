from django.urls import path
from .views import index
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(index, login_url='/login/'), name='index'),  # Redirects to login if not authenticated
]
