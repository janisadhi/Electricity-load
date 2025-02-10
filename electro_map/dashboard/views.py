from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='/login/')  # Redirect to login page if not authenticated
def index(request):
    return render(request, 'dashboard.html')
