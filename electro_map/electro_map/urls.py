from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from users.views import signup_view  # Assuming you have a 'users' app for authentication

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication routes
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),  # Ensure correct template path
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('signup/', signup_view, name='signup'),  # Custom signup view

    # App routes
    path('dashboard/', include('dashboard.urls')),  # Protect dashboard access
    path('dist/', include('logapp.urls')),  # Ensure logapp has its own prefix

    # Homepage as default
    path('', include('homepage.urls')),
]
