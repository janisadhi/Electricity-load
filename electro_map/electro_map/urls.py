from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from users.views import signup_view  # Assuming you have a 'users' app for authentication

urlpatterns = [
    path('admin/', admin.site.urls),

    # Protect dashboard access
    path('dashboard/', include('dashboard.urls')),

    # Authentication routes
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('signup/', signup_view, name='signup'),  # Custom signup view

    # Homepage
    path('', include('homepage.urls')),
]
